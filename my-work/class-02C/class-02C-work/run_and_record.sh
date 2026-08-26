#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_URL="${BASE_URL:-http://127.0.0.1:8000}"
APP_NAME="${APP_NAME:-workflow_agents}"
USER_ID="${USER_ID:-class02c-user}"
SESSION_ID="${SESSION_ID:-class02c-$(date +%Y%m%d-%H%M%S)}"
FIRST_MESSAGE="${FIRST_MESSAGE:-Hello}"
SECOND_MESSAGE="${1:-${SECOND_MESSAGE:-Ada Lovelace}}"

for command in curl jq; do
  if ! command -v "$command" >/dev/null 2>&1; then
    echo "Required command not found: $command"
    exit 1
  fi
done

run_message() {
  local message="$1"
  local output="$2"

  jq -n \
    --arg app "$APP_NAME" \
    --arg user "$USER_ID" \
    --arg session "$SESSION_ID" \
    --arg text "$message" \
    '{
      appName: $app,
      userId: $user,
      sessionId: $session,
      newMessage: {role: "user", parts: [{text: $text}]}
    }' \
    | curl -fsS -X POST "$BASE_URL/run" \
        -H 'Content-Type: application/json' \
        --data-binary @- \
    | tee "$output" \
    | jq 'map({timestamp, author, id, invocationId})'
}

echo "Available agents:"
curl -fsS "$BASE_URL/list-apps" | jq .

echo "Creating session $SESSION_ID"
curl -fsS -X POST \
  "$BASE_URL/apps/$APP_NAME/users/$USER_ID/sessions/$SESSION_ID" \
  -H 'Content-Type: application/json' \
  -d '{}' \
  | jq '{id, appName, userId}'

echo "Running first message: $FIRST_MESSAGE"
run_message "$FIRST_MESSAGE" "$SCRIPT_DIR/run-01.json"

echo "Running second message: $SECOND_MESSAGE"
run_message "$SECOND_MESSAGE" "$SCRIPT_DIR/run-02.json"

curl -fsS \
  "$BASE_URL/apps/$APP_NAME/users/$USER_ID/sessions/$SESSION_ID" \
  | tee "$SCRIPT_DIR/session.json" \
  | jq -c '.events[]' \
  > "$SCRIPT_DIR/events.jsonl"

cat > "$SCRIPT_DIR/last_session.env" <<EOF
BASE_URL=$BASE_URL
APP_NAME=$APP_NAME
USER_ID=$USER_ID
SESSION_ID=$SESSION_ID
EOF

echo "Recorded $(wc -l < "$SCRIPT_DIR/events.jsonl" | tr -d ' ') events"
echo "Recording: $SCRIPT_DIR/events.jsonl"

