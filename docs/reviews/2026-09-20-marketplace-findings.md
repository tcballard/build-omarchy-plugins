# Marketplace review follow-up — 20 September 2026

Compared with the [12 September audit](2026-09-12-marketplace-findings.md) and
13 September prose-warning follow-up. These are observed maintainer expectations,
not a claim of a newly announced policy. No changes to upstream SUBMISSION.md
or SECURITY.md were returned for the comparison window.

## Coverage

Enumerated 1,000 open repository records sorted by update time, continuing beyond
12 September 16:48 UTC. After excluding PRs and older records, collected all 3,559
comments from 896 open issues: 545 Plugin requests, 337 Verify requests, 14 others.
Expected and collected totals matched; no fetch failed; no thread exceeded the
100-comment page limit. There were 557 new HANCORE-linux comments across 407
threads. Indexed all records, then qualitatively read representative findings
and follow-ups. These are requests, not unique plugins or defect counts.

This review excludes now-closed submissions, older untouched issues and PR inline
comments. It is not an independent source audit of every plugin or a claim that
every comment was manually read. Findings refer to the linked reviewed snapshots;
later author claims do not establish resolution.

## Evidence and bundle response

| Reviewer evidence | Guidance/check added |
| --- | --- |
| [MFA CI](https://github.com/omacom/omarchy-plugin-marketplace/issues/7491#issuecomment-5741754091), [Mynah dependencies](https://github.com/omacom/omarchy-plugin-marketplace/issues/7255#issuecomment-5745951194) | Action/image/dependency pinning, actual installer lockfile use and least-privilege workflow review. |
| [AppSignal](https://github.com/omacom/omarchy-plugin-marketplace/issues/7141#issuecomment-5722655664), [Chezmoi Hound](https://github.com/omacom/omarchy-plugin-marketplace/issues/7526#issuecomment-5746267624) | Agent prompt/data separation, real file/tool exposure and fail-closed required isolation. |
| [OmaNomad](https://github.com/omacom/omarchy-plugin-marketplace/issues/5371#issuecomment-5745040622) | Independent trust for privileged verifier and expected artifact identity. |
| [Bitwarden](https://github.com/omacom/omarchy-plugin-marketplace/issues/3098#issuecomment-5744992291) | Fixed source must reach backend artifacts, defaults and minimum accepted versions. |
| [Artwork](https://github.com/omacom/omarchy-plugin-marketplace/issues/7180#issuecomment-5735649258), [transfers](https://github.com/omacom/omarchy-plugin-marketplace/issues/6068#issuecomment-5735045519) | Decoder failure, image limits and aggregate resource budgets. |
| [Workspace Summon](https://github.com/omacom/omarchy-plugin-marketplace/issues/7476#issuecomment-5746209569) | Agent settings/hooks/skills discovery beyond three special Markdown names. |
| [Coinbase](https://github.com/omacom/omarchy-plugin-marketplace/issues/7520#issuecomment-5741977697) | Reviewed broker source does not attest a mutable deployed credential service. |
| [Kamal baseline](https://github.com/omacom/omarchy-plugin-marketplace/issues/7656#issuecomment-5742922054) | Separate validator-pattern evidence from real runtime/setup behavior. |

The existing scaffold already pins Actions and declares permissions. Preserve
that behavior; the new lexical advisories identify common regressions in extended
plugin workflows. They do not parse all YAML, validate provenance or prove least
privilege. Agent-directory matches similarly request inspection, not automatic
rejection. Structural validity and security advisories remain separate.

No universal standard-installation gate was added: that form acknowledgment
predates the audit and applies to removing a manual-installation override.
The baseline contract is unchanged; no upstream contract pins were advanced.

Acceptance evidence is recorded in [ACCEPTANCE.md](../../evals/ACCEPTANCE.md).
The new handoff cases remain documented scenarios until actually exercised.
