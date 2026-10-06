# Focus scaffold result

Created `/workspace/scratch/plugin-template-evaluation/focus-starter` from the supplied `omarchy-plugin-scaffold` skill on 2026-10-06. The generated project is a GitHub-ready source starter, already initialized with the requested identity. Git and GitHub have not been initialized or configured.

| Field | Actual value |
| --- | --- |
| GitHub owner / repository | `example/omarchy-focus` |
| Slug | `focus` |
| Permanent plugin ID | `io.github.example.focus` |
| Display name / author | `Focus` / `Example` |
| Version / licence | `0.1.0` / MIT |
| Kind | `bar-widget` |
| Manifest entry point | `entryPoints.barWidget` → `StarterWidget.qml` |
| Runtime moduleName | `io.github.example.focus` |

The sample behavior is unchanged: each widget instance starts inactive; a left-button press toggles an in-memory boolean, the displayed circle, and the fixed starter tooltip. No persistence, service, network use, or additional Focus feature was added.

The output includes the manifest, QML entry point, README and credits, MIT licence, architecture/development/setup/release documents, project instructions, Workbench contract, issue/PR templates, SHA-pinned CI, source-release workflow, and development scripts. The source pin is `tcballard/omarchy-plugin-template@f99681e69937d21c2d4414ac9f65a0fd01fea714`, template version `0.1.0`, integration version `1`; `.template/source.json` records the two documented path-compatibility adjustments.

## Actual checks

| Check | Result |
| --- | --- |
| Node prerequisite | `v24.19.0`; requires 22+ |
| Generator snapshot verification and initialized-project check | Passed, exit 0 |
| Generated `./tests/run` | Passed, exit 0: structural/identity/link/CI-policy check and 5 reported Node tests |
| Installed toolkit `validate_plugin.py` | `VALID`, exit 0 |
| Toolkit `--json --security` | `valid: true`, no errors/warnings/findings, exit 0; advisory outcome `review-required` |
| Git boundary | No `.git` directory exists |

The five reported Node tests do **not** demonstrate runtime toggle behavior. In an initialized project, the test titled “initialization preserves edited files and refuses symlink destinations” returns early before those end-to-end assertions. Its reported pass is therefore narrower than its title suggests. Other tests cover input rejection, escaping, mocked repository policies, and refusal to overwrite existing policies.

The advisory scanner reports four capability records: authoring instructions in `AGENTS.md` and `.template/blueprint/AGENTS.md`, plus installer/package-manager mentions in `docs/SETUP.md`. The setup document describes future GitHub configuration and says no npm install is needed; it was not executed. These are review signals, not discovered runtime execution or security certification. The generated release script creates a full **source** archive, so installed runtime payload separation remains something to review before distribution.

Source identity outside Git: 42 files; SHA-256 inventory digest over sorted relative paths, file permission modes, and content hashes:

`d3123fec04f74159475a5645e437b9e327bb2085aed505fd79fd286ce4b459bf`

## Exact generation and validation commands

The destination was inspected and did not exist. All generated files and temporary test copies were confined to `/workspace/scratch/plugin-template-evaluation` using `TMPDIR`.

```bash
node --version
mkdir -p /workspace/scratch/plugin-template-evaluation/tmp
TMPDIR=/workspace/scratch/plugin-template-evaluation/tmp node /workspace/scratch/plugin-template-evaluation/scaffold-skill/scripts/new_repository.mjs --output /workspace/scratch/plugin-template-evaluation/focus-starter --owner example --repo omarchy-focus --slug focus --id io.github.example.focus --name Focus --author Example
```

Run from `/workspace/scratch/plugin-template-evaluation/focus-starter`:

```bash
TMPDIR=/workspace/scratch/plugin-template-evaluation/tmp ./tests/run
```

Additional installed toolkit checks:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 /root/.codex/skills/remote-skills/skill-6aa7b12e1e848191a43393b211ab54e8/scripts/validate_plugin.py /workspace/scratch/plugin-template-evaluation/focus-starter
PYTHONDONTWRITEBYTECODE=1 python3 /root/.codex/skills/remote-skills/skill-6aa7b12e1e848191a43393b211ab54e8/scripts/validate_plugin.py --json --security /workspace/scratch/plugin-template-evaluation/focus-starter
```

Tool availability checks returned no executable paths:

```bash
command -v omarchy || true
command -v qmllint || true
command -v omakit || true
```

Exact source-identity and Git-boundary check:

```bash
python3 - <<'PY'
from pathlib import Path
import hashlib
root = Path('/workspace/scratch/plugin-template-evaluation/focus-starter')
assert not (root / '.git').exists()
digest = hashlib.sha256()
files = sorted(p for p in root.rglob('*') if p.is_file())
for p in files:
    digest.update(p.relative_to(root).as_posix().encode() + b'\0')
    digest.update(f'{p.stat().st_mode & 0o777:03o}'.encode() + b'\0')
    digest.update(hashlib.sha256(p.read_bytes()).digest())
print(f'SHA-256 inventory digest ({len(files)} files, paths, modes and contents): {digest.hexdigest()}')
print('No .git directory exists.')
PY
```

## Remaining checks and boundaries

- Native `omarchy plugin validate /workspace/scratch/plugin-template-evaluation/focus-starter`, recording the actual installed Omarchy revision: unrun; Omarchy is unavailable.
- QML lint/parse against the target Qt/Quickshell and host imports: unrun; `qmllint` is unavailable.
- Live discovery, enablement, left-click toggle, horizontal/vertical layout, reload, disable/re-enable, monitor/theme changes, and clean installation/removal: unrun; no desktop changes were authorized or made. `docs/ACCEPTANCE.json` correctly remains `not-run`.
- Optional Omakit marketplace-baseline review: unrun; Omakit is unavailable. No marketplace acceptance is claimed.
- Actual GitHub CI, repository policy application, release/archive validation, and screenshots: unrun and outside this scaffold-only request. GitHub setup documentation retains generic template instructions; this local project's identity is already initialized.

No remote services were contacted, Git repositories initialized, Workbench registrations/trust actions performed, desktop changes made, or project files written outside the authorized directory. The supplied scaffold snapshot was not modified.
