#!/usr/bin/env python3
"""
Generate a screen-keyed design-QA report.

Inputs are reviewer JSON files, each containing either one screen verdict object
or a list of verdict objects. The script keeps this skill independent from older
behavioral-QA tc_id report tooling.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _as_screen_items(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]
    if not isinstance(payload, dict):
        return []
    if isinstance(payload.get("screens"), list):
        return [x for x in payload["screens"] if isinstance(x, dict)]
    if isinstance(payload.get("results"), list):
        return [x for x in payload["results"] if isinstance(x, dict)]
    return [payload]


def _screen_id(item: dict[str, Any], fallback: str) -> str:
    for key in ("screen", "screenId", "id", "route"):
        value = item.get(key)
        if isinstance(value, str) and value:
            return value
    return fallback


def _verdict(item: dict[str, Any]) -> str:
    value = item.get("verdict") or item.get("status") or item.get("result")
    if isinstance(value, str):
        value = value.upper()
        if value in {"PASS", "FAIL", "UNCERTAIN", "STATIC"}:
            return value
    findings = item.get("findings")
    if isinstance(findings, list) and findings:
        return "FAIL"
    return "PASS"


def _normalize_findings(item: dict[str, Any]) -> list[dict[str, Any]]:
    findings = item.get("findings", [])
    if isinstance(findings, dict):
        findings = [findings]
    if not isinstance(findings, list):
        return []

    normalized: list[dict[str, Any]] = []
    for raw in findings:
        if not isinstance(raw, dict):
            continue
        normalized.append(
            {
                "layer": raw.get("layer"),
                "severity": raw.get("severity"),
                "where": raw.get("where") or raw.get("selector") or raw.get("node"),
                "figmaValue": raw.get("figmaValue"),
                "renderedValue": raw.get("renderedValue"),
                "why": raw.get("why") or raw.get("reason"),
                "file": raw.get("file") or raw.get("fileLine"),
                "fix": raw.get("fix") or raw.get("fixCandidate"),
                "coverageNote": raw.get("coverageNote"),
            }
        )
    return normalized


def _coverage_from_screen_map(screen_map_path: Path | None) -> dict[str, Any]:
    if not screen_map_path:
        return {"mappedScreens": [], "gaps": {}}
    payload = _load_json(screen_map_path)
    screens = payload.get("screens", []) if isinstance(payload, dict) else []
    mapped = []
    for screen in screens:
        if isinstance(screen, dict):
            mapped.append(
                {
                    "screen": screen.get("screen"),
                    "route": screen.get("route"),
                    "figmaNode": screen.get("figmaNode"),
                    "confidence": (screen.get("match") or {}).get("confidence")
                    if isinstance(screen.get("match"), dict)
                    else None,
                }
            )
    gaps = payload.get("gaps", {}) if isinstance(payload, dict) else {}
    return {"mappedScreens": mapped, "gaps": gaps}


def build_report(inputs: list[Path], screen_map: Path | None) -> dict[str, Any]:
    coverage = _coverage_from_screen_map(screen_map)
    screens: dict[str, dict[str, Any]] = {}

    for idx, path in enumerate(inputs):
        for item in _as_screen_items(_load_json(path)):
            sid = _screen_id(item, path.stem if len(inputs) == 1 else f"{path.stem}-{idx}")
            findings = _normalize_findings(item)
            screens[sid] = {
                "screen": sid,
                "route": item.get("route"),
                "figmaNode": item.get("figmaNode") or item.get("nodeId"),
                "verdict": _verdict(item),
                "findings": findings,
                "keyMap": item.get("keyMap") or item.get("correspondence") or {},
                "source": str(path),
            }

    counts = Counter(screen["verdict"] for screen in screens.values())
    severity = Counter()
    for screen in screens.values():
        for finding in screen["findings"]:
            sev = finding.get("severity") or "UNKNOWN"
            severity[str(sev).upper()] += 1

    return {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "screenCount": len(screens),
            "pass": counts.get("PASS", 0),
            "fail": counts.get("FAIL", 0),
            "uncertain": counts.get("UNCERTAIN", 0),
            "static": counts.get("STATIC", 0),
            "findingsBySeverity": dict(severity),
        },
        "coverage": coverage,
        "screens": [screens[key] for key in sorted(screens)],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="*", type=Path, help="Reviewer JSON result files")
    parser.add_argument("--screen-map", type=Path, help="design-qa/<slug>/screen-map.json")
    parser.add_argument("--out", required=True, type=Path, help="Output report JSON path")
    args = parser.parse_args()

    report = build_report(args.inputs, args.screen_map)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
