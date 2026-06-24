#!/usr/bin/env python3
"""Validate visual-researcher reference_pack / asset_pack JSON."""

from __future__ import annotations

import json
import os
import sys
from collections import defaultdict
from pathlib import Path


CONFIDENCE = {"high", "medium", "low"}
MIN_REFERENCE_YEAR = 2024
ASSET_TYPES = {"brand", "icon", "image", "avatar", "lottie", "other"}
INGEST = {
    "svg:createNodeFromSvg",
    "raster:import_image",
    "lottie:poster-import-json-handoff",
    "handoff-only",
}


def grouped(items: list[dict]) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for item in items:
        groups[item["requestId"]].append(item)
    return groups


def fail(message: str) -> None:
    print(f"[visual-pack] ERROR: {message}", file=sys.stderr)
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


def validate_path(value: str, label: str) -> None:
    require(isinstance(value, str) and value, f"{label} must be a non-empty string")
    require(os.path.isabs(value), f"{label} must be absolute: {value!r}")
    require(os.path.exists(value), f"{label} does not exist: {value}")


def validate_references(items: object) -> None:
    require(isinstance(items, list) and items, "references must be a non-empty array")
    for i, ref in enumerate(items):
        where = f"references[{i}]"
        require(isinstance(ref, dict), f"{where} must be an object")
        for key in ("id", "requestId", "localPath", "sourceUrl", "product", "screen", "selectionRationale"):
            require(isinstance(ref.get(key), str) and ref[key], f"{where}.{key} is required")
        require(isinstance(ref.get("candidateRank"), int) and ref["candidateRank"] >= 1,
                f"{where}.candidateRank must be a positive integer")
        require(
            isinstance(ref.get("sourceYear"), int) and ref["sourceYear"] >= MIN_REFERENCE_YEAR,
            f"{where}.sourceYear must be an integer >= {MIN_REFERENCE_YEAR}",
        )
        validate_path(ref["localPath"], f"{where}.localPath")
        for key in ("patternsToTransfer", "trendSignals", "doNotCopy"):
            require(isinstance(ref.get(key), list) and ref[key], f"{where}.{key} must be non-empty")
            require(all(isinstance(x, str) and x for x in ref[key]), f"{where}.{key} must contain strings")
        require(ref.get("confidence") in CONFIDENCE, f"{where}.confidence must be high|medium|low")
    for request_id, candidates in grouped(items).items():
        if len(candidates) < 2:
            require(
                isinstance(candidates[0].get("singleCandidateReason"), str)
                and candidates[0]["singleCandidateReason"],
                f"references requestId={request_id!r} needs >=2 candidates or singleCandidateReason",
            )


def validate_assets(items: object) -> None:
    require(isinstance(items, list) and items, "assets must be a non-empty array")
    for i, asset in enumerate(items):
        where = f"assets[{i}]"
        require(isinstance(asset, dict), f"{where} must be an object")
        for key in ("id", "requestId", "format", "localPath", "sourceUrl", "selectionRationale"):
            require(isinstance(asset.get(key), str) and asset[key], f"{where}.{key} is required")
        require(isinstance(asset.get("candidateRank"), int) and asset["candidateRank"] >= 1,
                f"{where}.candidateRank must be a positive integer")
        require(asset.get("type") in ASSET_TYPES, f"{where}.type is invalid")
        require(asset.get("ingest") in INGEST, f"{where}.ingest is invalid")
        require(asset.get("confidence") in CONFIDENCE, f"{where}.confidence must be high|medium|low")
        validate_path(asset["localPath"], f"{where}.localPath")
        if asset.get("posterPath"):
            validate_path(asset["posterPath"], f"{where}.posterPath")
        if asset.get("type") == "brand" and asset.get("confidence") == "low":
            require(isinstance(asset.get("alternates"), list) and asset["alternates"],
                    f"{where} low-confidence brand assets require alternates")
    for request_id, candidates in grouped(items).items():
        if len(candidates) < 2:
            require(
                isinstance(candidates[0].get("singleCandidateReason"), str)
                and candidates[0]["singleCandidateReason"],
                f"assets requestId={request_id!r} needs >=2 candidates or singleCandidateReason",
            )


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: validate-visual-pack.py <pack.json>")
    data = load(Path(sys.argv[1]))
    mode = data.get("mode")
    require(mode in {"reference_pack", "asset_pack", "mixed"}, "mode must be reference_pack|asset_pack|mixed")
    if mode in {"reference_pack", "mixed"}:
        validate_references(data.get("references"))
    if mode in {"asset_pack", "mixed"}:
        validate_assets(data.get("assets"))
    print("[visual-pack] OK")


if __name__ == "__main__":
    main()
