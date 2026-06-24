# Bundled with the design-qa plugin.
"""
design_snapshot.py — structured design-fidelity snapshot of a LIVE rendered screen.

Captures per-element computed styles + bbox + Layer-1 invariants (truncation, offscreen,
zero-size) via Playwright. Reach (locale/role/auth/viewport) is manifest-driven — no stack
assumptions. Outputs are PII-sensitive; write to a gitignored directory, never commit.

CLI:
    # manifest-driven (preferred)
    python scripts/design_snapshot.py --manifest design-qa/example-app --screen customer-list \
        --out .tmp/design-qa/customer-list.snap.json --screenshot .tmp/design-qa/customer-list.png

    # ad-hoc (explicit flags, no manifest)
    python scripts/design_snapshot.py <url> --out snap.json --screenshot snap.png \
        --viewport 1600x960 --locale ko --set-storage role=admin
"""

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

# Reuse the login flow from the sibling behavioral-QA snapshot tool.
_HERE = Path(__file__).resolve().parent
_PROJECT_ROOT = _HERE.parent
_ENV_FILE = _PROJECT_ROOT / ".env"
if _ENV_FILE.exists():
    try:
        from dotenv import load_dotenv as _load_dotenv

        _load_dotenv(_ENV_FILE)
    except ImportError:
        pass


# --- in-page extractor: design facts + Layer-1 invariants -------------------
# Kept as a single evaluate() payload so the whole snapshot is one serialized read.
_EXTRACT_JS = r"""
() => {
  const STYLE_PROPS = [
    'color','backgroundColor','fontFamily','fontSize','fontWeight','lineHeight',
    'letterSpacing','textAlign','borderRadius','borderTopWidth','borderColor',
    'paddingTop','paddingRight','paddingBottom','paddingLeft','gap',
    'display','flexDirection','justifyContent','alignItems','boxShadow','opacity'
  ];
  const TAG_KEEP = new Set(['BUTTON','INPUT','A','TH','TD','H1','H2','H3','H4','H5',
                            'H6','LABEL','SELECT','TEXTAREA','IMG']);
  const ROLE_KEEP = new Set(['button','link','row','columnheader','cell','heading',
                             'textbox','tab','navigation','banner','main','table',
                             'grid','img','dialog','menuitem']);

  const ownText = (el) => {
    let t = '';
    for (const n of el.childNodes) if (n.nodeType === 3) t += n.textContent;
    return t.trim();
  };
  const visible = (el) => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    if (s.visibility === 'hidden' || s.display === 'none' || s.opacity === '0') return false;
    return r.width >= 1 && r.height >= 1;
  };
  const surface = (s) =>
    (s.backgroundColor && s.backgroundColor !== 'rgba(0, 0, 0, 0)') ||
    parseFloat(s.borderTopWidth) > 0 ||
    (s.boxShadow && s.boxShadow !== 'none');
  const keep = (el, s, txt) => {
    if (TAG_KEEP.has(el.tagName)) return true;
    const role = el.getAttribute('role');
    if (role && ROLE_KEEP.has(role)) return true;
    if (txt && surface(s)) return true;
    if (txt && el.children.length === 0) return true;       // leaf text
    return false;
  };

  // Tags whose text is source code / option lists, never visual layout text.
  const NONVISUAL = new Set(['SCRIPT','STYLE','NOSCRIPT','TEMPLATE','OPTION','HEAD','META','LINK','TITLE']);

  const nodes = [];
  const invariants = { truncated: [], offscreen: [], zeroSize: [] };
  const vw = window.innerWidth, vh = window.innerHeight;
  let idx = 0;

  for (const el of document.querySelectorAll('body *')) {
    if (NONVISUAL.has(el.tagName)) continue;
    const s = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    const txt = ownText(el);
    const allText = (el.textContent || '').trim();      // includes descendant text
    const hidden = s.display === 'none' || s.visibility === 'hidden';

    // Layer-1 invariants — computed on EVERY visible element (correspondence-free).
    // truncation: a CLIPPING box (overflow hidden/clip or ellipsis or line-clamp) whose
    // content overflows. Do NOT gate on own-text — the dominant pattern is a clipping cell
    // whose text lives in a child (<td class=ellipsis><span>…</span></td>). nowrap alone is
    // NOT a clip (overflow:visible spills but is fully readable), so it is excluded.
    if (!hidden && allText) {
      const clipX = s.overflowX === 'hidden' || s.overflowX === 'clip' ||
                    s.textOverflow === 'ellipsis';
      const lineClamp = s.webkitLineClamp && s.webkitLineClamp !== 'none';
      // scrollHeight>clientHeight is the real gate — an auto-height block sizes to its
      // content so it never trips, so no extra height guard is needed here.
      const clipY = lineClamp || s.overflowY === 'hidden' || s.overflowY === 'clip';
      const overX = clipX && el.scrollWidth > el.clientWidth + 1;
      const overY = clipY && el.scrollHeight > el.clientHeight + 1;
      if (overX || overY) {
        invariants.truncated.push({
          text: allText.slice(0, 40), tag: el.tagName.toLowerCase(),
          axis: overX ? (overY ? 'both' : 'x') : 'y',
          scrollW: el.scrollWidth, clientW: el.clientWidth,
          scrollH: el.scrollHeight, clientH: el.clientHeight,
          cls: (el.getAttribute('class') || '').slice(0, 60),
        });
      }
    }
    // intended-but-zero-size: rendered (not hidden) with own text yet 0 area.
    // Excludes display:none/visibility:hidden and non-visual tags (guarded above).
    if (!hidden && txt && (r.width < 1 || r.height < 1)) {
      invariants.zeroSize.push({ text: txt.slice(0, 40), tag: el.tagName.toLowerCase() });
    }
    // off-screen: an IN-FLOW (static/relative) sized element pushed outside the viewport.
    // Positioned (absolute/fixed) elements off-canvas are nearly always intentional —
    // sr-only labels (left:-9999px), drawers, popovers, carousels — so they are exempt to
    // avoid noise; a genuine layout defect pushes normal-flow content off-screen.
    const positioned = s.position === 'absolute' || s.position === 'fixed';
    if (!hidden && !positioned && r.width > 4 && r.height > 4 &&
        (r.right < 0 || r.bottom < 0 || r.left > vw + 1)) {
      invariants.offscreen.push({ text: txt.slice(0, 30), tag: el.tagName.toLowerCase(),
                                  x: Math.round(r.x), y: Math.round(r.y) });
    }

    if (!visible(el) || !keep(el, s, txt)) continue;
    const style = {};
    for (const p of STYLE_PROPS) style[p] = s[p];
    nodes.push({
      i: idx++,
      tag: el.tagName.toLowerCase(),
      role: el.getAttribute('role') || null,
      cls: (el.getAttribute('class') || '').slice(0, 80),
      text: txt.slice(0, 80),
      // drop query/fragment — signed/presigned asset URLs can carry tokens
      src: el.tagName === 'IMG' ? (el.getAttribute('src') || '').split('?')[0].split('#')[0].slice(0, 120) : null,
      bbox: { x: Math.round(r.x), y: Math.round(r.y),
              w: Math.round(r.width), h: Math.round(r.height) },
      style,
    });
  }

  return {
    title: document.title,
    // origin+pathname only — post-login URLs may carry session tokens in query/fragment
    url: location.origin + location.pathname,
    lang: document.documentElement.lang || null,
    viewport: { w: vw, h: vh },
    nodeCount: nodes.length,
    nodes,
    invariants,
  };
}
"""


def _apply_storage(context, pairs):
    """Seed localStorage before the app boots (locale/role/feature flags)."""
    for kv in pairs or []:
        if "=" not in kv:
            continue
        k, v = kv.split("=", 1)
        context.add_init_script(
            f"localStorage.setItem({json.dumps(k)}, {json.dumps(v)})"
        )


def _viewport_tuple(s):
    """Parse 'WxH' → (w, h), or None if unparseable. Non-raising (for manifest data)."""
    try:
        w, h = str(s).lower().split("x")
        return (int(w), int(h))
    except Exception:
        return None


def apply_url_params(url, params):
    """Return url with `params` merged into its query string (existing keys preserved).

    Used for view selectors only (locale/role) — NEVER for secrets; auth goes via cookie/storage.
    """
    if not params:
        return url
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query.update(params)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def build_reach_plan(project, screen):
    """Resolve a manifest's declared reach mechanisms into a normalized plan. Pure, no mutation.

    Reads `project.alignment.{locale,role}.mechanism` (localStorage | urlParam) + a screen's
    `reach.{role,locale,viewport}`, and routes each selector to the right transport. This is what
    makes the script project-bound without hardcoding a stack (e.g. the i18next key is the
    manifest's `locale.key`, not a constant).
    """
    alignment = (project or {}).get("alignment") or {}
    reach = (screen or {}).get("reach") or {}
    url_params, storage, context_locale = {}, [], None

    loc = alignment.get("locale") or {}
    lang = reach.get("locale") or loc.get("designLanguage")
    if lang:
        context_locale = lang  # always set the browser-context locale
        mechanism = loc.get("mechanism", "localStorage")
        key = loc.get("key") or "i18nextLng"
        if mechanism == "urlParam":
            url_params[key] = lang
        elif mechanism == "localStorage":
            storage.append(f"{key}={lang}")
        # 'env' / app-controlled: only the context locale is set here

    role = alignment.get("role") or {}
    role_val = reach.get("role")
    if role_val:
        mechanism = role.get("mechanism", "urlParam")
        param = role.get("param") or "role"
        if mechanism == "localStorage":
            storage.append(f"{param}={role_val}")
        elif mechanism == "urlParam":
            url_params[param] = role_val
        # 'auth'-gated roles are not a declarative selector → handled by build_auth_seed

    viewport = _viewport_tuple(reach.get("viewport")) if reach.get("viewport") else None
    return {"url_params": url_params, "storage": storage,
            "context_locale": context_locale, "viewport": viewport}


def build_auth_seed(project, env=None):
    """Resolve a manifest's declared auth into a seed. The SECRET comes from env (`valueEnv`),
    never from the tracked manifest. Returns None when no auth; a `missingEnv` marker (no value)
    when the env var is unset, so the caller can warn without leaking.
    """
    env = os.environ if env is None else env
    auth = ((project or {}).get("app") or {}).get("auth") or {}
    via = auth.get("via", "none")
    if not via or via == "none":
        return None
    value_env = auth.get("valueEnv")
    value = env.get(value_env) if value_env else None
    if not value:
        return {"via": via, "missingEnv": value_env}
    name = auth.get("name")
    if via == "cookie":
        return {"via": "cookie", "cookie": {"name": name, "value": value}}
    if via == "storage":
        return {"via": "storage", "storage": f"{name}={value}"}
    return {"via": via, "unsupported": True}


def load_manifest(slug_dir, screen_id):
    """Load (project.json, screen-entry) for `screen_id` from a `design-qa/<slug>/` directory."""
    base = Path(slug_dir)
    project = json.loads((base / "project.json").read_text(encoding="utf-8"))
    smap = json.loads((base / "screen-map.json").read_text(encoding="utf-8"))
    screen = next((s for s in smap.get("screens", []) if s.get("screen") == screen_id), None)
    if screen is None:
        raise SystemExit(f"screen '{screen_id}' not found in {base / 'screen-map.json'}")
    return project, screen


def _derive_url(project, screen):
    """Compose the target URL from the app's run url + the screen's route (both manifest fields).

    The manifest is untrusted data, and the result is fed to page.goto — so we allowlist the
    scheme to http(s). This refuses a malicious/typo `run.url` like `file:///etc/passwd` or an
    internal metadata endpoint before it can be fetched into the snapshot.
    """
    base = (((project or {}).get("app") or {}).get("run") or {}).get("url")
    if not base:
        return None
    route = screen.get("route") or ""
    url = base if not route else base.rstrip("/") + "/" + route.lstrip("/")
    if urlsplit(url).scheme not in ("http", "https"):
        raise SystemExit(
            f"refusing non-http(s) target url from manifest: {url!r} "
            f"(only http/https dev-server URLs are allowed)"
        )
    return url


def _origin(url):
    parts = urlsplit(url)
    return f"{parts.scheme}://{parts.netloc}"


def capture(
    url,
    out_path,
    screenshot_path=None,
    viewport=(1440, 900),
    locale=None,
    set_storage=None,
    login=False,
    base_url="",
    settle_ms=700,
    reach_plan=None,
    auth_seed=None,
):
    """Capture a structured design snapshot. Returns the snapshot dict.

    Reach is driven by `reach_plan` (from build_reach_plan over a manifest) when given; otherwise
    the explicit flags form an implicit plan (`--locale` seeds the i18next default key for
    back-compat). `auth_seed` (from build_auth_seed) injects a cookie/localStorage credential whose
    value came from env. `login=True` is a compatibility fallback to dom_snapshot's form-login flow.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError(
            "playwright required: pip install playwright && playwright install chromium"
        ) from exc

    storage = list(set_storage or [])
    url_params = {}
    context_locale = locale
    if reach_plan:
        storage = list(reach_plan.get("storage") or []) + storage
        url_params = dict(reach_plan.get("url_params") or {})
        context_locale = reach_plan.get("context_locale") or locale
    elif locale:
        # back-compat: bare --locale seeds the i18next default key (harmless if app ignores it)
        storage.append(f"i18nextLng={locale}")

    target_url = apply_url_params(url, url_params)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(
            viewport={"width": viewport[0], "height": viewport[1]},
            locale=context_locale or "en-US",
        )
        if auth_seed:
            if auth_seed.get("missingEnv"):
                print(f"[design_snapshot] auth skipped: env {auth_seed['missingEnv']} not set")
            elif auth_seed.get("via") == "cookie":
                cookie = dict(auth_seed["cookie"])
                cookie.setdefault("url", _origin(target_url))
                ctx.add_cookies([cookie])
            elif auth_seed.get("via") == "storage":
                storage.append(auth_seed["storage"])
        _apply_storage(ctx, storage)
        page = ctx.new_page()

        if login and base_url:  # compatibility fallback; declarative auth_seed is preferred
            try:
                from dom_snapshot import _login_page

                _login_page(page, base_url)
            except Exception as exc:  # login is best-effort; report, don't abort
                print(f"[design_snapshot] login skipped: {exc}")

        try:
            try:
                page.goto(target_url, wait_until="networkidle", timeout=30_000)
            except Exception as exc:
                if "timeout" not in str(exc).lower():
                    raise
            page.wait_for_timeout(settle_ms)

            snapshot = page.evaluate(_EXTRACT_JS)
            if screenshot_path:
                page.screenshot(path=screenshot_path, full_page=True)
                snapshot["screenshot"] = str(screenshot_path)
        finally:
            browser.close()

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(snapshot, fh, ensure_ascii=False, indent=2)
    return snapshot


def _parse_viewport(s):
    try:
        w, h = s.lower().split("x")
        return (int(w), int(h))
    except Exception:
        raise argparse.ArgumentTypeError("viewport must be WxH, e.g. 1600x960")


def _parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("url", nargs="?", default=None,
                   help="Target screen URL (omit when using --manifest; derived from run url + route)")
    p.add_argument("--manifest", default=None,
                   help="design-qa/<slug>/ dir — reach (locale/role/auth/viewport) comes from it")
    p.add_argument("--screen", default=None, help="screen id in the manifest's screen-map.json")
    p.add_argument("--out", required=True, help="Output JSON path")
    p.add_argument("--screenshot", default=None, help="Screenshot PNG path")
    p.add_argument("--viewport", type=_parse_viewport, default=None,
                   help="WxH; explicit overrides the manifest. Default (no manifest): 1440x900")
    p.add_argument("--locale", default=None, help="Align app i18n to the Figma design language, e.g. ko")
    p.add_argument("--set-storage", action="append", default=[],
                   help="Seed localStorage key=value before boot (repeatable), e.g. role=admin")
    p.add_argument("--login", action="store_true", help="Legacy: run dom_snapshot form-login first")
    p.add_argument("--base-url", default=os.environ.get("QA_BASE_URL", ""))
    p.add_argument("--settle-ms", type=int, default=700)
    return p.parse_args(argv)


def main(argv=None):
    a = _parse_args(argv)
    url, viewport, reach_plan, auth_seed = a.url, a.viewport, None, None

    if a.manifest:
        if not a.screen:
            raise SystemExit("--manifest requires --screen")
        project, screen = load_manifest(a.manifest, a.screen)
        reach_plan = build_reach_plan(project, screen)
        auth_seed = build_auth_seed(project)
        if not url:
            url = _derive_url(project, screen)
            if not screen.get("route"):
                # never silently capture the wrong screen — a null route lands on the app root
                print(f"[design_snapshot] WARNING: screen '{a.screen}' has no `route` in "
                      f"screen-map.json — capturing the app root ({url}), NOT the screen. "
                      f"Pin the route to fix this.", file=sys.stderr)
        viewport = viewport or reach_plan.get("viewport")  # explicit flag wins over manifest

    if not url:
        raise SystemExit("a target url is required (positional, or derivable via --manifest)")
    viewport = viewport or (1440, 900)

    snap = capture(
        url=url, out_path=a.out, screenshot_path=a.screenshot,
        viewport=viewport, locale=a.locale, set_storage=a.set_storage,
        login=a.login, base_url=a.base_url, settle_ms=a.settle_ms,
        reach_plan=reach_plan, auth_seed=auth_seed,
    )
    inv = snap["invariants"]
    print(f"nodes={snap['nodeCount']} lang={snap['lang']} "
          f"truncated={len(inv['truncated'])} offscreen={len(inv['offscreen'])} "
          f"zeroSize={len(inv['zeroSize'])}")
    print(f"json={a.out}" + (f" screenshot={a.screenshot}" if a.screenshot else ""))


if __name__ == "__main__":
    main()
