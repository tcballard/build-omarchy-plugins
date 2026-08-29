#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fixture="$root/demo/fixtures/example.json"

python3 -m json.tool "$fixture" >/dev/null
printf 'Demo fixture is valid: %s\n' "$fixture"
printf 'Build a reversible live-shell harness before claiming screenshot evidence.\n'
