# VENDORED into the design-qa plugin from qa-automation/scripts/dom_snapshot.py.
# Canonical source lives at the repo root; imported by design_snapshot.py for login flows.
# Keep this copy in sync when the canonical script changes.
"""
dom_snapshot.py — Takes a URL and returns a DOM snapshot (accessibility tree +
key selectors) for LLM consumption. Caches results to avoid redundant browser
launches.

CLI:
    python scripts/dom_snapshot.py <url> [--cache-dir dom_cache] [--force-refresh]
"""

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

# Load .env from project root (two levels up from scripts/)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_ENV_FILE = _PROJECT_ROOT / ".env"
if _ENV_FILE.exists():
    try:
        from dotenv import load_dotenv as _load_dotenv
        _load_dotenv(_ENV_FILE)
    except ImportError:
        pass


def _url_hash(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()[:12]


def _build_selector(element_handle) -> str:
    """Build a best selector: prefer #id > [aria-label] > [name] > [placeholder]."""
    el_id = element_handle.get_attribute("id")
    if el_id:
        return f"#{el_id}"

    aria_label = element_handle.get_attribute("aria-label")
    if aria_label:
        return f'[aria-label="{aria_label}"]'

    name = element_handle.get_attribute("name")
    if name:
        return f'[name="{name}"]'

    placeholder = element_handle.get_attribute("placeholder")
    if placeholder:
        return f'[placeholder="{placeholder}"]'

    return ""


def _collect_interactive_elements(page) -> list:
    """Collect interactive elements from the page."""
    selectors = [
        "button",
        "input",
        "select",
        "textarea",
        "a[href]",
        '[role="button"]',
        '[role="link"]',
    ]

    elements = []
    seen_selectors = set()

    for selector in selectors:
        handles = page.query_selector_all(selector)
        for handle in handles:
            try:
                tag = handle.evaluate("el => el.tagName.toLowerCase()")
                role = handle.get_attribute("role") or ""
                text_content = (handle.inner_text() or "").strip()[:50]
                best_selector = _build_selector(handle)

                if best_selector and best_selector in seen_selectors:
                    continue
                if best_selector:
                    seen_selectors.add(best_selector)

                elements.append(
                    {
                        "tag": tag,
                        "role": role,
                        "text": text_content,
                        "selector": best_selector,
                    }
                )
            except Exception:
                # Skip elements that throw during inspection (e.g. detached nodes)
                continue

    return elements


def _login_page(page, base_url: str) -> None:
    """
    Log in using env vars if credentials are set.
    Uses role-based selectors — stable against React-generated IDs.
    """
    email = os.environ.get("QA_HQ_EMAIL") or os.environ.get("QA_USER_A_EMAIL")
    password = os.environ.get("QA_HQ_PASSWORD") or os.environ.get("QA_USER_A_PASSWORD")
    if not (email and password):
        return

    page.goto(base_url + "/login", wait_until="networkidle", timeout=30_000)

    # Try role-based first (works for ARIA-labeled inputs like "DDMS ID")
    try:
        ddms_field = page.get_by_role("textbox", name="DDMS ID")
        if ddms_field.count() > 0:
            # Use type() not fill() — React apps need character-level events for onChange
            ddms_field.click()
            ddms_field.type(email, delay=30)
            pw = page.get_by_role("textbox", name="Password")
            pw.click()
            pw.type(password, delay=30)
            page.wait_for_timeout(300)
            page.get_by_role("button", name="Login").click()
            page.wait_for_timeout(3000)
            return
    except Exception:
        pass

    # Fallback: generic email/password selectors
    try:
        id_input = page.locator("input[type='email'], input[name='email'], #email").first
        id_input.click()
        id_input.type(email, delay=30)
        pw_input = page.locator("input[type='password'], input[name='password'], #password").first
        pw_input.click()
        pw_input.type(password, delay=30)
        page.wait_for_timeout(300)
        page.locator("button[type='submit'], input[type='submit'], #submit, .login-btn").first.click()
        page.wait_for_timeout(3000)
    except Exception:
        pass


def get_snapshot(
    url: str,
    cache_dir: str = "dom_cache",
    force_refresh: bool = False,
    login: bool = False,
    base_url: str = "",
) -> dict:
    """
    Return a DOM snapshot dict for the given URL.

    Keys:
        accessibility_tree    — result of page.accessibility.snapshot()
        interactive_elements  — list of {tag, role, text, selector}
        page_title            — page title
        current_url           — final URL after redirects
    """
    cache_path = Path(cache_dir) / f"{_url_hash(url)}.json"

    if not force_refresh and cache_path.exists():
        with cache_path.open("r", encoding="utf-8") as fh:
            return json.load(fh)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError(
            "playwright is required: pip install playwright && playwright install chromium"
        ) from exc

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()

        if login and base_url:
            _login_page(page, base_url)

        try:
            page.goto(url, wait_until="networkidle", timeout=30_000)
        except Exception as exc:
            # Tolerate timeout on networkidle — snapshot whatever loaded
            if "timeout" not in str(exc).lower():
                raise

        accessibility_tree = page.accessibility.snapshot()
        interactive_elements = _collect_interactive_elements(page)
        page_title = page.title()
        current_url = page.url

        browser.close()

    snapshot = {
        "accessibility_tree": accessibility_tree,
        "interactive_elements": interactive_elements,
        "page_title": page_title,
        "current_url": current_url,
    }

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    with cache_path.open("w", encoding="utf-8") as fh:
        json.dump(snapshot, fh, ensure_ascii=False, indent=2)

    return snapshot


def _parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Capture a DOM snapshot (accessibility tree + key selectors) for a URL."
    )
    parser.add_argument("url", help="Target URL to snapshot")
    parser.add_argument(
        "--cache-dir",
        default="dom_cache",
        help="Directory for cached snapshots (default: dom_cache)",
    )
    parser.add_argument(
        "--force-refresh",
        action="store_true",
        help="Ignore cache and re-fetch the page",
    )
    parser.add_argument(
        "--login",
        action="store_true",
        help="Log in before snapshotting (uses QA_HQ_EMAIL/PASSWORD env vars)",
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("QA_BASE_URL", ""),
        help="Base URL for login (default: $QA_BASE_URL)",
    )
    return parser.parse_args(argv)


def main(argv=None) -> None:
    args = _parse_args(argv)
    snapshot = get_snapshot(
        url=args.url,
        cache_dir=args.cache_dir,
        force_refresh=args.force_refresh,
        login=args.login,
        base_url=args.base_url,
    )
    print(json.dumps(snapshot, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
