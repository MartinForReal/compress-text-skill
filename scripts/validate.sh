#!/usr/bin/env bash
#
# Validate the repository before publishing:
#   - JSON manifests parse
#   - skill structure, manifest wiring, and eval datasets are well-formed
#   - (optional) `claude plugin validate` when the Claude CLI is installed
#
# Usage: ./scripts/validate.sh

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

echo "==> Validating JSON manifests"
python3 - <<'PY'
import json, sys
for f in (".claude-plugin/plugin.json", ".claude-plugin/marketplace.json"):
    json.load(open(f))
    print(f"    ok: {f}")
PY

echo "==> Running evaluation suite (static checks)"
python3 evals/run_evals.py

if command -v claude >/dev/null 2>&1; then
  echo "==> Running 'claude plugin validate --strict'"
  claude plugin validate . --strict
else
  echo "==> Skipping 'claude plugin validate' (Claude CLI not installed)"
fi

echo "==> All checks passed"
