#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RECORDING="${1:-$SCRIPT_DIR/events.jsonl}"
DELAY="${2:-0.75}"

if [[ ! -s "$RECORDING" ]]; then
  echo "Recording not found or empty: $RECORDING"
  exit 1
fi

while IFS= read -r event; do
  jq -r '
    ([.content.parts[]? | keys[]] | unique | join(",")) as $parts
    | "[\(.author // "unknown")] \(if $parts == "" then "event" else $parts end)"
  ' <<<"$event"
  sleep "$DELAY"
done < "$RECORDING"

