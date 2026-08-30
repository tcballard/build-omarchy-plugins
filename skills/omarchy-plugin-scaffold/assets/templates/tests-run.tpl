#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 "$root/scripts/validate_manifest.py" "$root"
bash -n "$root/demo/run"
python3 -m json.tool "$root/demo/fixtures/example.json" >/dev/null

if command -v omarchy >/dev/null 2>&1; then
  omarchy plugin validate "$root"
fi

printf 'All portable plugin checks passed.\n'
