#!/usr/bin/env python3
"""Index a downloaded GitHub issue/comment corpus; never execute submitted content.

Input: issues/*.json and comments/*.json (GitHub REST arrays). Labels are text
mentions, not vulnerability findings. Outputs preserve URLs and content digests.
"""
from __future__ import annotations
import argparse
import collections
import csv
import hashlib
import json
import re
from pathlib import Path

THEMES = {
    "resource-bounds": r"unbounded|uncapped|byte.{0,15}(?:cap|limit|ceiling)|producer.side|cardinality|before.{0,20}(?:collect|pars|buffer)",
    "plain-text": r"AutoText|Text\.PlainText|rich.text",
    "file-identity": r"symlink|no.follow|dir_fd|descriptor.relative|TOCTOU|path.{0,12}traversal",
    "process-lifetime": r"watchdog|reap|process.group|PID.{0,8}reuse|PGID|wall.clock|hard deadline",
    "executable-environment": r"ambient.{0,12}PATH|PATH.shadow|inherited.{0,15}environment|trusted.{0,20}executable|executable.identity|closed.{0,12}environment",
    "injection": r"(?:command|shell|argument|option|code|config).{0,12}injection|shell.string|bash -c|sh -c",
    "credentials": r"credential|bearer|mnemonic|recovery phrase|secret.{0,20}argv|token.{0,20}(?:mode|file|argv)",
    "agent-control-payload": r"agent.control|agent/session|HANDOFF\.md|CLAUDE\.md|AGENTS\.md|prompt.injection",
    "privilege-supply-chain": r"pkexec|sudoers|polkit|root.owned|supply.chain|attestation|unverified.{0,15}binary",
    "snapshot-form": r"does not match|no longer matches|stale.{0,20}(?:baseline|SHA|validation)|headings|form.{0,20}(?:parse|changed)|fresh.{0,15}validation",
    "duplicate-workflow": r"duplicate|supersed|reconciliation|finalization|deployment.{0,15}fail",
    "network-policy": r"redirect|SSRF|same.origin|https.{0,12}allowlist|URL.{0,15}(?:scheme|policy|valid)",
}

def records(directory: Path):
    result = {}
    for path in sorted(directory.glob("*.json")):
        values = json.loads(path.read_text())
        if not isinstance(values, list):
            raise ValueError(f"not a REST array: {path}")
        for value in values:
            old = result.get(value["id"])
            if old is None or value.get("updated_at", "") >= old.get("updated_at", ""):
                result[value["id"]] = value
    return list(result.values())

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("corpus", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    issues = records(args.corpus / "issues")
    comments = records(args.corpus / "comments")
    counts = collections.Counter(int(c["issue_url"].rsplit("/", 1)[1]) for c in comments)
    args.output.mkdir(parents=True, exist_ok=True)
    with (args.output / "issue-index.csv").open("w", newline="") as f:
        w = csv.writer(f); w.writerow(["number", "kind", "state", "expected_comments", "collected_comments", "url", "body_sha256"])
        for i in sorted(issues, key=lambda i:i["number"]):
            kind = "pull-request" if "pull_request" in i else "plugin" if i["title"].startswith("[Plugin]") else "verify" if i["title"].startswith("[Verify]") else "other"
            w.writerow([i["number"],kind,i["state"],i["comments"],counts[i["number"]],i["html_url"],hashlib.sha256((i.get("body") or "").encode()).hexdigest()])
    mentions = collections.defaultdict(set)
    human = [c for c in comments if c["user"]["login"] == "HANCORE-linux"]
    with (args.output / "hancore-index.csv").open("w", newline="") as f:
        w = csv.writer(f);w.writerow(["comment_id","issue","created_at","themes","explicit_disposition","url","body_sha256"])
        for c in sorted(human, key=lambda c:c["id"]):
            body = c.get("body") or ""
            labels = [k for k,p in THEMES.items() if re.search(p,body,re.I)]
            for label in labels: mentions[label].add(int(c["issue_url"].rsplit("/",1)[1]))
            disposition = re.findall(r'"disposition"\s*:\s*"([^"]+)"',body)
            w.writerow([c['id'],c['issue_url'].rsplit('/',1)[1],c['created_at'],';'.join(labels),';'.join(disposition),c['html_url'],hashlib.sha256(body.encode()).hexdigest()])
    summary = {
        "repository":"omacom/omarchy-plugin-marketplace", "collected_date":"2026-09-12",
        "entries":len(issues),"pull_requests":sum("pull_request" in i for i in issues),
        "plugin_title_entries":sum(i['title'].startswith('[Plugin]') and 'pull_request' not in i for i in issues),
        "verify_title_entries":sum(i['title'].startswith('[Verify]') and 'pull_request' not in i for i in issues),
        "expected_comments_at_inventory":sum(i['comments'] for i in issues),"collected_unique_comments":len(comments),
        "missing_comments":{str(i['number']):i['comments']-counts[i['number']] for i in issues if counts[i['number']]<i['comments']},
        "extra_comments_since_inventory":{str(i['number']):counts[i['number']]-i['comments'] for i in issues if counts[i['number']]>i['comments']},
        "hancore_comments":len(human),"hancore_distinct_issues":len({c['issue_url'] for c in human}),
        "bot_comments":sum(c['user']['login']=='github-actions[bot]' for c in comments),
        "theme_distinct_threads_mentioning":dict(sorted((k,len(v)) for k,v in mentions.items())),
        "interpretation":"Overlapping keyword mentions across all Hancore comments, including resolved findings and approvals; NOT defect or rejection rates. Title counts are requests, NOT unique plugins. No independent source audit of submitted repositories.",
    }
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__ == '__main__': main()
