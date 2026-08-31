from __future__ import annotations

import json
import re
import struct
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
SUBMISSION = REPO / "submission"
ADAPTER = REPO / "plugins/build-omarchy-plugins"


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[:24]
    if len(data) != 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError(f"not a PNG: {path}")
    return struct.unpack(">II", data[16:24])


class SubmissionPacketTests(unittest.TestCase):
    def test_routing_evals_are_balanced_unique_and_reference_real_skills(self) -> None:
        payload = json.loads((SUBMISSION / "evals.json").read_text(encoding="utf-8"))
        self.assertEqual(1, payload["schemaVersion"])
        self.assertEqual("build-omarchy-plugins", payload["plugin"])
        self.assertEqual("0.2.3", payload["version"])
        cases = payload["cases"]
        self.assertEqual(10, len(cases))
        self.assertEqual(len(cases), len({case["id"] for case in cases}))
        self.assertEqual(5, sum(case["shouldTrigger"] for case in cases))
        self.assertEqual(5, sum(not case["shouldTrigger"] for case in cases))

        skills = {path.name for path in (REPO / "skills").iterdir() if path.is_dir()}
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertTrue(case["prompt"].strip())
                self.assertEqual(case["shouldTrigger"], bool(case["expectedSkills"]))
                self.assertLessEqual(set(case["expectedSkills"]), skills)
                if case["shouldTrigger"]:
                    self.assertTrue(case["expectedResultShape"].strip())
                    self.assertTrue(case["fixture"].strip())
                else:
                    self.assertTrue(case["safeFallback"].strip())
                    self.assertTrue(case["reason"].strip())

    def test_starter_prompts_and_portal_identity_match_plugin_metadata(self) -> None:
        manifest = json.loads((ADAPTER / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        starter = (SUBMISSION / "starter-prompts.md").read_text(encoding="utf-8")
        prompts = re.findall(r"^\d+\. (.+)$", starter, re.MULTILINE)
        self.assertEqual(manifest["interface"]["defaultPrompt"], prompts)

        portal = (SUBMISSION / "portal-field-map.md").read_text(encoding="utf-8")
        for value in (
            manifest["interface"]["displayName"],
            manifest["interface"]["shortDescription"],
            manifest["interface"]["websiteURL"],
            manifest["interface"]["privacyPolicyURL"],
            manifest["interface"]["termsOfServiceURL"],
            manifest["version"],
        ):
            self.assertIn(value, portal)

    def test_artwork_and_policy_assets_exist_at_declared_shapes(self) -> None:
        assets = ADAPTER / "assets"
        self.assertEqual((1024, 1024), png_dimensions(assets / "app-icon.png"))
        self.assertEqual((1600, 900), png_dimensions(assets / "workflow.png"))
        self.assertLess((assets / "app-icon.png").stat().st_size, 1024 * 1024)
        self.assertTrue((assets / "build-omarchy-plugins-small.svg").is_file())
        for policy in ("LICENSE", "PRIVACY.md", "SECURITY.md", "SUPPORT.md", "TERMS.md"):
            self.assertTrue((REPO / policy).is_file(), policy)

    def test_release_copy_describes_the_hardened_boundary(self) -> None:
        notes = (SUBMISSION / "release-notes.md").read_text(encoding="utf-8")
        for phrase in (
            "provider-neutral", "OpenCode", "transactional", "SPDX 2.3",
            "Linux, macOS, and Windows", "cannot publish",
        ):
            self.assertIn(phrase, notes)
        checklist = (SUBMISSION / "submission-checklist.md").read_text(encoding="utf-8")
        self.assertIn("- [ ] Merge the reviewed release pull request", checklist)
        self.assertIn("- [ ] Upload the skills archive", checklist)


if __name__ == "__main__":
    unittest.main()
