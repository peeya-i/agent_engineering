#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MANIFEST="$SCRIPT_DIR/golden-source.sha256"

if [[ ! -f "$MANIFEST" ]]; then
  echo "Missing checksum manifest: $MANIFEST"
  exit 1
fi

# Linux ships sha256sum; macOS ships shasum.
if command -v sha256sum >/dev/null 2>&1; then
  CHECK=(sha256sum -c)
elif command -v shasum >/dev/null 2>&1; then
  CHECK=(shasum -a 256 -c)
else
  echo "Neither sha256sum nor shasum is available; skipping the integrity check."
  exit 0
fi

cd "$PACKAGE_ROOT"
"${CHECK[@]}" "$MANIFEST"
echo "PASS: the golden application source and configuration are unmodified."
