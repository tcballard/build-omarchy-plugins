from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
WORKFLOWS = REPO / ".github/workflows"


class GovernanceTests(unittest.TestCase):
    def test_pinned_contract_bytes_use_portable_line_endings(self) -> None:
        attributes = (REPO / ".gitattributes").read_text(encoding="utf-8")
        self.assertIn("contracts/*.json text eol=lf", attributes.splitlines())

    def test_contract_ledger_is_strict_and_offline_check_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(REPO / "scripts/check_contracts.py"), "--json"],
            cwd=REPO, text=True, capture_output=True, check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(4, len(payload["contracts"]))
        workbench = next(
            item for item in payload["contracts"]
            if item["name"] == "Omarchy Plugin Workbench project definition"
        )
        self.assertTrue(workbench["vendoredVerified"])

        ledger = (REPO / "contracts/upstream-contracts.json").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as temporary:
            broken = Path(temporary) / "contracts.json"
            broken.write_text(ledger.replace('"schemaVersion": 1,', '"schemaVersion": 1, "schemaVersion": 1,'), encoding="utf-8")
            rejected = subprocess.run(
                [sys.executable, str(REPO / "scripts/check_contracts.py"), "--ledger", str(broken), "--json"],
                cwd=REPO, text=True, capture_output=True, check=False,
            )
            self.assertEqual(1, rejected.returncode)
            self.assertIn("duplicate JSON key", json.loads(rejected.stdout)["error"])

    def test_every_workflow_action_is_immutably_pinned(self) -> None:
        workflows = sorted(WORKFLOWS.glob("*.yml"))
        self.assertEqual({"ci.yml", "codeql.yml", "contract-drift.yml", "release-draft.yml"}, {path.name for path in workflows})
        for path in workflows:
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertTrue(text.startswith("name:"))
                self.assertIn("\non:\n", text)
                self.assertIn("\njobs:\n", text)
                uses = re.findall(r"^\s*- uses:\s+([^\s#]+)", text, re.MULTILINE)
                self.assertTrue(uses)
                for action in uses:
                    self.assertRegex(action, r"^[^@]+@[0-9a-f]{40}$")

    def test_ci_has_full_matrix_and_stable_required_check(self) -> None:
        text = (WORKFLOWS / "ci.yml").read_text(encoding="utf-8")
        for os_name in ("ubuntu-latest", "macos-latest", "windows-latest"):
            self.assertIn(os_name, text)
        for version in ('"3.11"', '"3.12"', '"3.13"'):
            self.assertIn(version, text)
        self.assertIn("name: Validate workflows", text)
        self.assertIn("actions/setup-go@924ae3a1cded613372ab5595356fb5720e22ba16", text)
        self.assertIn("actionlint/cmd/actionlint@914e7df21a07ef503a81201c76d2b11c789d3fca", text)
        self.assertIn('actionlint" .github/workflows/*.yml', text)
        self.assertIn("name: CI / Required", text)
        self.assertIn("needs: [test, workflow-lint]", text)

    def test_release_automation_is_draft_only_and_rechecks_remote_identity(self) -> None:
        workflow = (WORKFLOWS / "release-draft.yml").read_text(encoding="utf-8")
        self.assertIn("--draft", workflow)
        self.assertNotIn("--draft=false", workflow)
        self.assertNotIn("gh release edit", workflow)
        self.assertGreaterEqual(workflow.count("git ls-remote origin refs/heads/main"), 2)
        self.assertGreaterEqual(workflow.count('git ls-remote origin "refs/tags/$TAG"'), 2)
        self.assertIn('DIST_A: ${{ runner.temp }}/release-dist-a', workflow)
        self.assertIn('DIST_B: ${{ runner.temp }}/release-dist-b', workflow)
        self.assertIn('diff -qr "$DIST_A" "$DIST_B"', workflow)
        self.assertIn('diff -qr "$DIST_A" "$download"', workflow)
        self.assertNotIn('releases/tags/$TAG', workflow)
        self.assertEqual(2, workflow.count('gh release view "$TAG" --json isDraft --jq .isDraft'))
        self.assertIn('for attempt in 1 2 3 4 5', workflow)
        self.assertIn('gh release download "$TAG" --dir "$download" --clobber', workflow)
        self.assertIn("CI / Required", workflow)

        runbook = (REPO / "docs/RELEASING.md").read_text(encoding="utf-8")
        self.assertIn("immutable-releases", runbook)
        self.assertIn("--draft=false", runbook)
        self.assertIn("gh release verify", runbook)
        self.assertIn("Never move a release tag", runbook)

    def test_contribution_policy_requires_pull_requests(self) -> None:
        policy = (REPO / "CONTRIBUTING.md").read_text(encoding="utf-8")
        self.assertIn("Never commit directly to `main`", policy)
        self.assertIn("every change goes", policy)
        self.assertIn("CI / Required", policy)


if __name__ == "__main__":
    unittest.main()
