# Quattro alignment and lighter portable skills

Reviewed on 17 October 2026 against Omarchy Quattro `cce8b1c971df64a7610b818ff8819e4bea04584a`. Base toolkit commit: `e3a45f8b444034ae7ed1f437ea71b4ece677ac95`.

## Changes and scope

All twelve stable skill names remain. Their combined SKILL.md text falls from 6,884 to 2,892 whitespace-delimited words (58% less, including frontmatter). Repeated workflow/handoff boilerplate was removed; conditional test/release/submission mechanics remain linked references. Instructions require no particular provider, harness, planner, tool registry or worker topology. Optional host packaging and companion tools remain available.

The Agents-panel starter is documented accurately as a default-agent prompt using Omarchy's built-in guide. Personal built-in customization uses a user-owned clone. Palette templates use Commons.Color; generator and validator accept the six current bar sections. Translation guidance covers plugin catalogs, reactive bindings, plurals, numbers/dates and RTL without silently raising an existing plugin's minimum host version.

## Executed evidence

- `./scripts/test`: passed, including 79 Python tests, Node repository-template tests, all twelve skill routes, generated adapter parity, contract ledger validation and deterministic package checks.
- `python3 -m unittest discover -s tests -p test_quattro_alignment.py -v`: passed. Each of six section values round-trips through real generation and strict validation; unsupported values fail. All five generated visual kinds avoid unqualified palette access.
- `git diff --check`: passed. Changed Markdown local links resolve.
- Independent source review found no outstanding actionable findings; it checked refreshed Omarchy contract digests, placement values, generated palette references and changed links.

## Independent task smoke test

A fresh agent session received only the scaffold, widget and QML skill paths and a user-style task: build a fixed 25:00 widget toggling Focus/Paused with horizontal/vertical forms, no network, persistence, panel or service. It wrote to a fresh temporary directory and did not modify the toolkit or a live desktop.

Observed output: root `manifest.json`, hosted `BarWidget.qml`, per-instance toggle state, inline horizontal text and stacked vertical text; ID `io.github.example.focus`, author Example. Generated `./tests/run` passed its manifest, shell-syntax and fixture checks. Source inspection confirmed the requested implementation. Those portable checks do not execute Qt click handling or prove rendering.

Canonical skill-tree digest: `111a2659dc838291aaf56a379ea02c8fc297f5f8eb59b2b00dfa6231d8fc2acc`. Fixture-tree digest: `c3de13f26b92ba47c17c385c66200b1722ab292238796920f63a5dd1337910e9`. Digests hash sorted relative path, NUL, bytes, NUL for each regular file, excluding Git metadata and Python bytecode caches. Evaluation host: Codex Work Mode, Linux; exact model/version/reasoning settings not exposed. Agent used ordinary file/shell operations with no service or desktop access. This is one smoke test, not a measured cross-harness improvement or a live Omarchy acceptance run.

## Unrun checks

No Omarchy executable, qmllint or live Quattro display was available. Hosted imports, Qt 6.12 rendering, actual pointer/keyboard interaction, tray popout geometry, language switching, regional/plural fallbacks and RTL remain target-host acceptance work. The new Agents-panel, clone, translations and tray evaluation cases are documented; this review does not claim their live execution or a marketplace/release publication.
