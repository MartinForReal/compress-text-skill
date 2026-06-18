#!/usr/bin/env bash
#
# Build a distributable Agent Skill bundle (.zip) for the compress-text skill.
#
# The bundle is a zip archive whose top-level entry is the `compress-text/`
# directory containing SKILL.md (plus any references/scripts/assets). This is
# the format accepted by claude.ai (Settings > Capabilities > Skills), the
# Claude Skills API, Claude Platform on AWS, and Microsoft Foundry.
#
# Usage:
#   ./scripts/build-skill-bundle.sh
#
# Output:
#   dist/compress-text-skill.zip

set -euo pipefail

SKILL_NAME="compress-text"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_DIR="${ROOT_DIR}/skills/${SKILL_NAME}"
DIST_DIR="${ROOT_DIR}/dist"
OUTPUT="${DIST_DIR}/${SKILL_NAME}-skill.zip"

if [[ ! -f "${SKILL_DIR}/SKILL.md" ]]; then
  echo "error: ${SKILL_DIR}/SKILL.md not found" >&2
  exit 1
fi

mkdir -p "${DIST_DIR}"
rm -f "${OUTPUT}"

# Zip from the skills/ directory so the archive contains "compress-text/SKILL.md".
# Exclude OS cruft and VCS metadata.
( cd "${ROOT_DIR}/skills" \
  && zip -r -X "${OUTPUT}" "${SKILL_NAME}" \
       -x '*.DS_Store' -x '__MACOSX/*' -x '*/.git/*' >/dev/null )

echo "Built ${OUTPUT}"
unzip -l "${OUTPUT}"
