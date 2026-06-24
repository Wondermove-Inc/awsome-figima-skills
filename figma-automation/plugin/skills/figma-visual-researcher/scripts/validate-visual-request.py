#!/usr/bin/env python3
"""Validate builder -> visual-researcher request JSON."""

from __future__ import annotations

import json
import sys
from pathlib import Path


MIN_BRIEF_CHARS = 120
MIN_REFERENCE_YEAR = 2024
REQUEST_ARRAYS = ("referenceRequests", "assetRequests")
ASSET_TYPES = {"brand", "icon", "image", "avatar", "lottie", "other"}
COMMON_TEXT_FIELDS = ("targetScreen", "usage", "placement", "targetSize")
COMMON_LIST_FIELDS = ("styleKeywords", "desiredQualities", "mustHave", "avoid")


def fail(message: str) -> None:
    print(f"[visual-request] ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as exc:  # noqa: BLE001 - CLI should surface concise validation failure.
        fail(f"cannot read JSON: {exc}")
    require(isinstance(data, dict), "top-level JSON must be an object")
    return data


def validate_brief(item: dict, where: str) -> None:
    brief = item.get("brief")
    require(isinstance(brief, str) and brief.strip(), f"{where}.brief is required")
    require(
        len(brief.strip()) >= MIN_BRIEF_CHARS,
        f"{where}.brief must be detailed natural language (>= {MIN_BRIEF_CHARS} chars)",
    )


def require_non_empty_string(item: dict, field: str, where: str) -> None:
    value = item.get(field)
    require(isinstance(value, str) and value.strip(), f"{where}.{field} is required")


def require_non_empty_string_list(item: dict, field: str, where: str) -> None:
    value = item.get(field)
    require(isinstance(value, list) and value, f"{where}.{field} must be a non-empty list")
    for i, entry in enumerate(value):
        require(
            isinstance(entry, str) and entry.strip(),
            f"{where}.{field}[{i}] must be a non-empty string",
        )


def require_source_preference(item: dict, where: str) -> None:
    value = item.get("sourcePreference")
    if isinstance(value, str):
        require(bool(value.strip()), f"{where}.sourcePreference is required")
        return
    if isinstance(value, list):
        require(bool(value), f"{where}.sourcePreference must be non-empty")
        for i, entry in enumerate(value):
            require(
                isinstance(entry, str) and entry.strip(),
                f"{where}.sourcePreference[{i}] must be a non-empty string",
            )
        return
    fail(f"{where}.sourcePreference is required")


def validate_candidate_count(item: dict, where: str) -> None:
    value = item.get("candidateCount")
    require(isinstance(value, int), f"{where}.candidateCount is required")
    require(2 <= value <= 6, f"{where}.candidateCount must be between 2 and 6")


def validate_min_source_year(item: dict, where: str) -> None:
    value = item.get("minSourceYear")
    require(isinstance(value, int), f"{where}.minSourceYear is required")
    require(value >= MIN_REFERENCE_YEAR, f"{where}.minSourceYear must be >= {MIN_REFERENCE_YEAR}")


def validate_common_request(item: dict, where: str) -> None:
    for field in COMMON_TEXT_FIELDS:
        require_non_empty_string(item, field, where)
    for field in COMMON_LIST_FIELDS:
        require_non_empty_string_list(item, field, where)
    require_source_preference(item, where)
    validate_candidate_count(item, where)
    validate_brief(item, where)


def validate_reference_request(item: object, index: int) -> None:
    where = f"referenceRequests[{index}]"
    require(isinstance(item, dict), f"{where} must be an object")
    require(isinstance(item.get("id"), str) and item["id"], f"{where}.id is required")
    require(item.get("mode") in (None, "reference_pack"), f"{where}.mode must be reference_pack")
    require_non_empty_string(item, "referenceKind", where)
    require(isinstance(item.get("screens"), list) and item["screens"], f"{where}.screens must be non-empty")
    validate_min_source_year(item, where)
    require_non_empty_string_list(item, "trendFocus", where)
    validate_common_request(item, where)


def validate_asset_request(item: object, index: int) -> None:
    where = f"assetRequests[{index}]"
    require(isinstance(item, dict), f"{where} must be an object")
    require(isinstance(item.get("id"), str) and item["id"], f"{where}.id is required")
    require(item.get("mode") in (None, "asset_pack"), f"{where}.mode must be asset_pack")
    require(item.get("type") in ASSET_TYPES, f"{where}.type is invalid")
    require_non_empty_string(item, "assetKind", where)
    require_non_empty_string(item, "query", where)
    require(
        (isinstance(item.get("preferredFormat"), str) and item["preferredFormat"].strip())
        or (isinstance(item.get("outputFormats"), list) and item["outputFormats"]),
        f"{where}.preferredFormat or {where}.outputFormats is required",
    )
    if isinstance(item.get("outputFormats"), list):
        for i, entry in enumerate(item["outputFormats"]):
            require(
                isinstance(entry, str) and entry.strip(),
                f"{where}.outputFormats[{i}] must be a non-empty string",
            )
    validate_common_request(item, where)


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: validate-visual-request.py <request.json>")
    data = load(Path(sys.argv[1]))
    require(data.get("blocked") is True, "blocked must be true")
    require(data.get("reason") == "visual_research_required", "reason must be visual_research_required")
    present = [name for name in REQUEST_ARRAYS if isinstance(data.get(name), list) and data[name]]
    require(present, "at least one non-empty referenceRequests or assetRequests array is required")
    for i, item in enumerate(data.get("referenceRequests") or []):
        validate_reference_request(item, i)
    for i, item in enumerate(data.get("assetRequests") or []):
        validate_asset_request(item, i)
    print("[visual-request] OK")


if __name__ == "__main__":
    main()
