#!/usr/bin/env python3
"""Unit tests for validate-visual-pack.py."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validate-visual-pack.py"


class VisualPackValidatorTest(unittest.TestCase):
    def run_validator(self, payload: dict, tmp: Path) -> subprocess.CompletedProcess[str]:
        pack = tmp / "pack.json"
        pack.write_text(json.dumps(payload), encoding="utf-8")
        return subprocess.run(
            ["python3", str(VALIDATOR), str(pack)],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_reference_pack_requires_transfer_and_do_not_copy(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            image_1 = tmp / "ref-1.png"
            image_2 = tmp / "ref-2.png"
            image_1.write_bytes(b"fake")
            image_2.write_bytes(b"fake")
            result = self.run_validator(
                {
                    "mode": "reference_pack",
                    "references": [
                        {
                            "id": "ref-example",
                            "requestId": "dashboard-refs",
                            "candidateRank": 1,
                            "localPath": str(image_1),
                            "sourceUrl": "https://example.com",
                            "product": "Example",
                            "screen": "Dashboard",
                            "sourceYear": 2025,
                            "selectionRationale": "Best dense dashboard candidate.",
                            "patternsToTransfer": ["dense rows"],
                            "trendSignals": ["bottom sheet filtering", "compressed status row"],
                            "doNotCopy": ["pixel layout"],
                            "confidence": "high",
                        },
                        {
                            "id": "ref-example-alt",
                            "requestId": "dashboard-refs",
                            "candidateRank": 2,
                            "localPath": str(image_2),
                            "sourceUrl": "https://example.com/alt",
                            "product": "Example",
                            "screen": "Dashboard alternate",
                            "sourceYear": 2024,
                            "selectionRationale": "Alternate information hierarchy candidate.",
                            "patternsToTransfer": ["compact filter bar"],
                            "trendSignals": ["large rounded filter chips", "progressive disclosure"],
                            "doNotCopy": ["exact brand"],
                            "confidence": "medium",
                        }
                    ],
                },
                tmp,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_reference_pack_rejects_pre_2024_sources(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            image_1 = tmp / "ref-1.png"
            image_2 = tmp / "ref-2.png"
            image_1.write_bytes(b"fake")
            image_2.write_bytes(b"fake")
            result = self.run_validator(
                {
                    "mode": "reference_pack",
                    "references": [
                        {
                            "id": "ref-old",
                            "requestId": "dashboard-refs",
                            "candidateRank": 1,
                            "localPath": str(image_1),
                            "sourceUrl": "https://example.com/old",
                            "product": "Example",
                            "screen": "Old Dashboard",
                            "sourceYear": 2023,
                            "selectionRationale": "Old candidate that should not pass.",
                            "patternsToTransfer": ["dense rows"],
                            "trendSignals": ["legacy card grid"],
                            "doNotCopy": ["pixel layout"],
                            "confidence": "high",
                        },
                        {
                            "id": "ref-new",
                            "requestId": "dashboard-refs",
                            "candidateRank": 2,
                            "localPath": str(image_2),
                            "sourceUrl": "https://example.com/new",
                            "product": "Example",
                            "screen": "New Dashboard",
                            "sourceYear": 2024,
                            "selectionRationale": "New candidate.",
                            "patternsToTransfer": ["compact filter bar"],
                            "trendSignals": ["large rounded filter chips"],
                            "doNotCopy": ["exact brand"],
                            "confidence": "medium",
                        },
                    ],
                },
                tmp,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("sourceYear", result.stderr)

    def test_reference_pack_rejects_missing_trend_signals(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            image_1 = tmp / "ref-1.png"
            image_2 = tmp / "ref-2.png"
            image_1.write_bytes(b"fake")
            image_2.write_bytes(b"fake")
            result = self.run_validator(
                {
                    "mode": "reference_pack",
                    "references": [
                        {
                            "id": "ref-example",
                            "requestId": "dashboard-refs",
                            "candidateRank": 1,
                            "localPath": str(image_1),
                            "sourceUrl": "https://example.com",
                            "product": "Example",
                            "screen": "Dashboard",
                            "sourceYear": 2024,
                            "selectionRationale": "Candidate without trend signals.",
                            "patternsToTransfer": ["dense rows"],
                            "doNotCopy": ["pixel layout"],
                            "confidence": "high",
                        },
                        {
                            "id": "ref-example-alt",
                            "requestId": "dashboard-refs",
                            "candidateRank": 2,
                            "localPath": str(image_2),
                            "sourceUrl": "https://example.com/alt",
                            "product": "Example",
                            "screen": "Dashboard alternate",
                            "sourceYear": 2024,
                            "selectionRationale": "Alternate candidate.",
                            "patternsToTransfer": ["compact filter bar"],
                            "trendSignals": ["progressive disclosure"],
                            "doNotCopy": ["exact brand"],
                            "confidence": "medium",
                        },
                    ],
                },
                tmp,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("trendSignals", result.stderr)

    def test_asset_pack_rejects_missing_ingest(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            asset = tmp / "brand.svg"
            asset.write_text("<svg />", encoding="utf-8")
            result = self.run_validator(
                {
                    "mode": "asset_pack",
                    "assets": [
                        {
                            "id": "brand-example",
                            "requestId": "brand-example",
                            "candidateRank": 1,
                            "type": "brand",
                            "format": "svg",
                            "localPath": str(asset),
                            "sourceUrl": "https://example.com/brand.svg",
                            "selectionRationale": "Only direct SVG candidate.",
                            "confidence": "high",
                        }
                    ],
                },
                tmp,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("ingest", result.stderr)

    def test_asset_pack_rejects_single_candidate_without_reason(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            asset = tmp / "brand.svg"
            asset.write_text("<svg />", encoding="utf-8")
            result = self.run_validator(
                {
                    "mode": "asset_pack",
                    "assets": [
                        {
                            "id": "brand-example",
                            "requestId": "brand-example",
                            "candidateRank": 1,
                            "type": "brand",
                            "format": "svg",
                            "localPath": str(asset),
                            "ingest": "svg:createNodeFromSvg",
                            "sourceUrl": "https://example.com/brand.svg",
                            "selectionRationale": "Only direct SVG candidate.",
                            "confidence": "high",
                        }
                    ],
                },
                tmp,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("singleCandidateReason", result.stderr)

    def test_asset_pack_accepts_multiple_candidates_for_one_request(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            svg = tmp / "brand.svg"
            png = tmp / "brand.png"
            svg.write_text("<svg />", encoding="utf-8")
            png.write_bytes(b"fake")
            result = self.run_validator(
                {
                    "mode": "asset_pack",
                    "assets": [
                        {
                            "id": "brand-example-svg",
                            "requestId": "brand-example",
                            "candidateRank": 1,
                            "type": "brand",
                            "format": "svg",
                            "localPath": str(svg),
                            "ingest": "svg:createNodeFromSvg",
                            "sourceUrl": "https://example.com/brand.svg",
                            "selectionRationale": "Best vector candidate for small UI.",
                            "confidence": "high",
                        },
                        {
                            "id": "brand-example-png",
                            "requestId": "brand-example",
                            "candidateRank": 2,
                            "type": "brand",
                            "format": "png",
                            "localPath": str(png),
                            "ingest": "raster:import_image",
                            "sourceUrl": "https://example.com/brand.png",
                            "selectionRationale": "Raster fallback if SVG import renders poorly.",
                            "confidence": "medium",
                        },
                    ],
                },
                tmp,
            )
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
