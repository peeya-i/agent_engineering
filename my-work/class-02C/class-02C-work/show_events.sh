#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RECORDING="${1:-$SCRIPT_DIR/events.jsonl}"

if [[ ! -s "$RECORDING" ]]; then
  echo "Recording not found or empty: $RECORDING"
  exit 1
fi

printf 'SEQ\tTIME\tAUTHOR\tPART TYPES\tSTATE KEYS\n'

jq -rs '
  to_entries[]
  | .key as $index
  | .value
  | ([.content.parts[]? | keys[]] | unique | join(",")) as $parts
  | ((.actions.stateDelta // {}) | keys | join(",")) as $state
  | [
      ($index + 1),
      (.timestamp // ""),
      (.author // "unknown"),
      (if $parts == "" then "event" else $parts end),
      (if $state == "" then "-" else $state end)
    ]
  | @tsv
' "$RECORDING"

