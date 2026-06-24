#!/usr/bin/env python3
"""Unit tests for validate-visual-request.py."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validate-visual-request.py"


DETAILED_BRIEF = (
    "Find a premium 3D or dimensional trophy visual for a mobile amateur sports tournament result "
    "screen. It should feel celebratory, athletic, and polished, with a strong silhouette at small size, "
    "transparent background, and no childish cartoon styling or busy confetti that fights Korean text."
)

VALID_COMMON = {
    "targetScreen": "match result empty state",
    "usage": "hero visual above the result summary and primary CTA",
    "placement": "top-of-screen hero illustration",
    "targetSize": "96-140px rendered size inside a 390px mobile frame, transparent background",
    "sourcePreference": ["Iconify colorful sets", "official public asset libraries", "LottieFiles poster fallback"],
    "candidateCount": 3,
    "styleKeywords": ["3D", "premium", "athletic", "celebratory", "small-size legible"],
    "desiredQualities": ["strong silhouette", "clear against Korean text", "not childish", "mobile-safe"],
    "mustHave": ["transparent background", "usable at 96px", "local file handoff"],
    "avoid": ["flat line icon", "cartoon trophy", "busy confetti", "watermarked stock"],
}


class VisualRequestValidatorTest(unittest.TestCase):
    def run_validator(self, payload: dict, tmp: Path) -> subprocess.CompletedProcess[str]:
        request = tmp / "request.json"
        request.write_text(json.dumps(payload), encoding="utf-8")
        return subprocess.run(
            ["python3", str(VALIDATOR), str(request)],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_accepts_detailed_asset_brief(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            result = self.run_validator(
                {
                    "blocked": True,
                    "reason": "visual_research_required",
                    "assetRequests": [
                        {
                            "id": "hero-trophy",
                            "mode": "asset_pack",
                            "type": "icon",
                            "assetKind": "dimensional hero trophy icon",
                            "query": "premium 3D trophy celebration icon",
                            "preferredFormat": "svg-or-png",
                            "brief": DETAILED_BRIEF,
                            **VALID_COMMON,
                        }
                    ],
                },
                Path(d),
            )
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_accepts_detailed_reference_request(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            result = self.run_validator(
                {
                    "blocked": True,
                    "reason": "visual_research_required",
                    "referenceRequests": [
                        {
                            "id": "payment-status-refs",
                            "mode": "reference_pack",
                            "referenceKind": "real mobile payment status screenshots",
                            "brief": (
                                "Find real mobile payment-status UI references for a Korean fintech or sports "
                                "commerce flow. I need production screenshots that show success, pending, and "
                                "failure states with calm status hierarchy, compact receipt detail, and restrained "
                                "confirmation feedback instead of decorative concept art."
                            ),
                            "screens": ["payment success", "payment pending", "payment failure"],
                            "minSourceYear": 2024,
                            "trendFocus": ["modern fintech status hierarchy", "compact receipt rows"],
                            **{
                                **VALID_COMMON,
                                "targetScreen": "payment status screen",
                                "usage": "pattern reference before composing the payment completion screen",
                                "placement": "full-screen mobile UI reference",
                                "targetSize": "mobile app screenshots near 390x844 or source listing screenshots that can be inspected at phone scale",
                                "sourcePreference": ["App Store screenshots", "Google Play screenshots", "official product pages"],
                                "styleKeywords": ["calm", "high-trust", "fintech", "receipt-like", "minimal celebration"],
                                "desiredQualities": ["clear transaction outcome", "legible detail rows", "credible production UI"],
                                "mustHave": ["real product screenshot", "source URL", "patterns to transfer"],
                                "avoid": ["landing-page mockups", "generic success clipart", "Dribbble concept art"],
                            },
                        }
                    ],
                },
                Path(d),
            )
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_vague_reference_brief(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            result = self.run_validator(
                {
                    "blocked": True,
                    "reason": "visual_research_required",
                    "referenceRequests": [
                        {
                            "id": "payment-refs",
                            "mode": "reference_pack",
                            "referenceKind": "mobile payment screenshots",
                            "screens": ["payment success"],
                            "minSourceYear": 2024,
                            "trendFocus": ["modern mobile status hierarchy"],
                            **VALID_COMMON,
                            "brief": "Find good payment refs.",
                        }
                    ],
                },
                Path(d),
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("brief", result.stderr)

    def test_rejects_missing_target_size(self) -> None:
        payload_common = {**VALID_COMMON}
        payload_common.pop("targetSize")
        with tempfile.TemporaryDirectory() as d:
            result = self.run_validator(
                {
                    "blocked": True,
                    "reason": "visual_research_required",
                    "assetRequests": [
                        {
                            "id": "hero-trophy",
                            "mode": "asset_pack",
                            "type": "icon",
                            "assetKind": "dimensional hero trophy icon",
                            "query": "premium 3D trophy celebration icon",
                            "preferredFormat": "svg-or-png",
                            "brief": DETAILED_BRIEF,
                            **payload_common,
                        }
                    ],
                },
                Path(d),
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("targetSize", result.stderr)

    def test_rejects_empty_style_keywords(self) -> None:
        payload_common = {**VALID_COMMON, "styleKeywords": []}
        with tempfile.TemporaryDirectory() as d:
            result = self.run_validator(
                {
                    "blocked": True,
                    "reason": "visual_research_required",
                    "assetRequests": [
                        {
                            "id": "hero-trophy",
                            "mode": "asset_pack",
                            "type": "icon",
                            "assetKind": "dimensional hero trophy icon",
                            "query": "premium 3D trophy celebration icon",
                            "preferredFormat": "svg-or-png",
                            "brief": DETAILED_BRIEF,
                            **payload_common,
                        }
                    ],
                },
                Path(d),
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("styleKeywords", result.stderr)

    def test_rejects_reference_request_before_2024(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            result = self.run_validator(
                {
                    "blocked": True,
                    "reason": "visual_research_required",
                    "referenceRequests": [
                        {
                            "id": "payment-refs",
                            "mode": "reference_pack",
                            "referenceKind": "mobile payment screenshots",
                            "brief": (
                                "Find real mobile payment-status UI references for a Korean fintech flow with "
                                "clear success and failure hierarchy, compact receipt rows, polished production "
                                "UI, and modern interaction patterns that can guide the builder."
                            ),
                            "screens": ["payment success"],
                            "minSourceYear": 2023,
                            "trendFocus": ["modern mobile status hierarchy"],
                            **VALID_COMMON,
                        }
                    ],
                },
                Path(d),
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("minSourceYear", result.stderr)

    def test_rejects_reference_request_without_trend_focus(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            result = self.run_validator(
                {
                    "blocked": True,
                    "reason": "visual_research_required",
                    "referenceRequests": [
                        {
                            "id": "payment-refs",
                            "mode": "reference_pack",
                            "referenceKind": "mobile payment screenshots",
                            "brief": (
                                "Find real mobile payment-status UI references for a Korean fintech flow with "
                                "clear success and failure hierarchy, compact receipt rows, polished production "
                                "UI, and modern interaction patterns that can guide the builder."
                            ),
                            "screens": ["payment success"],
                            "minSourceYear": 2024,
                            **VALID_COMMON,
                        }
                    ],
                },
                Path(d),
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("trendFocus", result.stderr)


if __name__ == "__main__":
    unittest.main()
