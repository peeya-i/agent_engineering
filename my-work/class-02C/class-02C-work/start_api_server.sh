#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PROJECT_ROOT="$PACKAGE_ROOT"
PROJECT_ID="${1:-${PROJECT_ID:-${GOOGLE_CLOUD_PROJECT:-}}}"

if [[ ! -d "$PROJECT_ROOT" ]]; then
  echo "Missing $PROJECT_ROOT"
  exit 1
fi

if [[ ! -f "$PROJECT_ROOT/.env" ]]; then
  echo "Missing $PROJECT_ROOT/.env"
  echo "Create it from a template first. See Task 2 of class_02C_instructions.md:"
  echo "  cp .env.vertex.example .env   # or: cp .env.api-key.example .env"
  exit 1
fi

if [[ ! -f "$PROJECT_ROOT/.venv/bin/activate" ]]; then
  echo "Missing project virtual environment."
  echo "See Task 1 of class_02C_instructions.md:"
  echo "  python3 -m venv .venv && source .venv/bin/activate && python -m pip install -e ."
  exit 1
fi

if [[ -z "$PROJECT_ID" ]]; then
  echo "Set PROJECT_ID or pass it as the first argument."
  echo "Example: ./start_api_server.sh my-project-id"
  exit 1
fi

source "$PROJECT_ROOT/.venv/bin/activate"

set -a
source "$PROJECT_ROOT/.env"
set +a

export GOOGLE_CLOUD_PROJECT="$PROJECT_ID"
export OTEL_SERVICE_NAME="${OTEL_SERVICE_NAME:-class-02c-live}"
# CHANGE ADDED PEEYA to include project ID
export OTEL_RESOURCE_ATTRIBUTES="${OTEL_RESOURCE_ATTRIBUTES:-deployment.environment=classroom,class.name=02C,gcp.project_id=$PROJECT_ID}"
export OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT="${OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT:-NO_CONTENT}"

exec adk api_server \
  --otel_to_cloud \
  --no-reload \
  --port "${ADK_PORT:-8000}" \
  --session_service_uri="sqlite:///$SCRIPT_DIR/sessions.db" \
  "$PROJECT_ROOT/adk_multiagent_systems"
