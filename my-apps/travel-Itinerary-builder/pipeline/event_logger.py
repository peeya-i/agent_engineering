"""JSON Event Logger for recording all model messages, responses, and tool calls."""

from datetime import datetime, timezone
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.plugins import BasePlugin
from google.adk.tools import BaseTool, ToolContext

logger = logging.getLogger(__name__)

# Top-level events.json path
DEFAULT_EVENTS_FILE = Path(__file__).resolve().parent.parent / "events.json"


def serialize_for_json(obj: Any) -> Any:
    """Recursively serializes objects to JSON-compatible data structures."""
    if obj is None:
        return None
    if isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, (list, tuple, set)):
        return [serialize_for_json(item) for item in obj]
    if isinstance(obj, dict):
        return {str(k): serialize_for_json(v) for k, v in obj.items()}
    if hasattr(obj, "model_dump"):
        try:
            return serialize_for_json(obj.model_dump(mode="json"))
        except Exception:
            pass
    if hasattr(obj, "to_dict"):
        try:
            return serialize_for_json(obj.to_dict())
        except Exception:
            pass
    if hasattr(obj, "__dict__"):
        try:
            return serialize_for_json(obj.__dict__)
        except Exception:
            pass
    return str(obj)


def append_event_to_json(
    event_entry: Dict[str, Any],
    file_path: Optional[Path] = None
) -> None:
    """Appends a structured event entry to the events.json file."""
    target_path = file_path or DEFAULT_EVENTS_FILE
    target_path = Path(target_path).resolve()

    events_list: List[Dict[str, Any]] = []

    # Read existing events if the file exists and is valid JSON
    if target_path.exists():
        try:
            with open(target_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    existing = json.loads(content)
                    if isinstance(existing, list):
                        events_list = existing
                    elif isinstance(existing, dict):
                        events_list = [existing]
        except Exception as e:
            logger.warning("Could not read existing %s (%s). Recreating.", target_path, e)
            events_list = []

    clean_entry = serialize_for_json(event_entry)
    events_list.append(clean_entry)

    # Atomically/safely write back to file
    try:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = target_path.with_suffix(".tmp")
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(events_list, f, indent=2, ensure_ascii=False)
        temp_path.replace(target_path)
    except Exception as e:
        logger.error("Failed to write event to %s: %s", target_path, e)


class JsonEventLoggerPlugin(BasePlugin):
    """ADK Plugin to capture model messages, model responses, and tool calls into events.json."""

    def __init__(
        self,
        name: str = "json_event_logger",
        output_file: Optional[Path] = None
    ):
        super().__init__(name=name)
        self.output_file = output_file or DEFAULT_EVENTS_FILE

    async def before_model_callback(
        self,
        *,
        callback_context: Any,
        llm_request: LlmRequest
    ) -> Optional[LlmResponse]:
        """Records outgoing messages and configuration sent to the model."""
        agent_name = getattr(callback_context, "agent_name", "unknown_agent")

        # Extract contents / prompt messages
        contents = getattr(llm_request, "contents", None)
        model_name = getattr(llm_request, "model", None)
        config = getattr(llm_request, "config", None)

        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": "model_request",
            "agent": agent_name,
            "model": model_name,
            "request_contents": serialize_for_json(contents),
            "config": serialize_for_json(config),
        }
        append_event_to_json(entry, self.output_file)
        return None

    async def after_model_callback(
        self,
        *,
        callback_context: Any,
        llm_response: LlmResponse
    ) -> Optional[LlmResponse]:
        """Records incoming responses and tool/function calls received from the model."""
        agent_name = getattr(callback_context, "agent_name", "unknown_agent")

        content = getattr(llm_response, "content", None)
        model_version = getattr(llm_response, "model_version", None)
        usage_metadata = getattr(llm_response, "usage_metadata", None)
        finish_reason = getattr(llm_response, "finish_reason", None)

        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": "model_response",
            "agent": agent_name,
            "model_version": model_version,
            "response_content": serialize_for_json(content),
            "finish_reason": str(finish_reason) if finish_reason else None,
            "usage_metadata": serialize_for_json(usage_metadata),
        }
        append_event_to_json(entry, self.output_file)
        return None

    async def before_tool_callback(
        self,
        *,
        tool: BaseTool,
        tool_args: Dict[str, Any],
        tool_context: ToolContext
    ) -> Optional[Dict[str, Any]]:
        """Records tool invocations before execution."""
        agent_name = getattr(tool_context, "agent_name", "unknown_agent")
        tool_name = getattr(tool, "name", str(tool))

        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": "tool_call",
            "agent": agent_name,
            "tool_name": tool_name,
            "tool_arguments": serialize_for_json(tool_args),
        }
        append_event_to_json(entry, self.output_file)
        return None

    async def after_tool_callback(
        self,
        *,
        tool: BaseTool,
        tool_args: Dict[str, Any],
        tool_context: ToolContext,
        result: Any
    ) -> Optional[Dict[str, Any]]:
        """Records tool outputs and responses after execution."""
        agent_name = getattr(tool_context, "agent_name", "unknown_agent")
        tool_name = getattr(tool, "name", str(tool))

        state_dict = {}
        if hasattr(tool_context, "state"):
            if hasattr(tool_context.state, "to_dict"):
                try:
                    state_dict = tool_context.state.to_dict()
                except Exception:
                    state_dict = getattr(tool_context.state, "_value", {})
            elif hasattr(tool_context.state, "_value"):
                state_dict = getattr(tool_context.state, "_value", {})

        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": "tool_response",
            "agent": agent_name,
            "tool_name": tool_name,
            "tool_arguments": serialize_for_json(tool_args),
            "tool_result": serialize_for_json(result),
            "state_snapshot": serialize_for_json(state_dict)
        }
        append_event_to_json(entry, self.output_file)
        return None
