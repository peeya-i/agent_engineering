"""Small, reusable model logging callbacks."""

from __future__ import annotations

import logging

from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse

LOGGER = logging.getLogger(__name__)


def log_query_to_model(
    callback_context: CallbackContext,
    llm_request: LlmRequest,
) -> None:
    """Log text in the latest user message sent to a model."""
    if not llm_request.contents or llm_request.contents[-1].role != "user":
        return None

    for part in llm_request.contents[-1].parts or []:
        if part.text:
            LOGGER.info("[query to %s] %s", callback_context.agent_name, part.text)
    return None


def log_model_response(
    callback_context: CallbackContext,
    llm_response: LlmResponse,
) -> None:
    """Log model text and function-call names."""
    if not llm_response.content or not llm_response.content.parts:
        return None

    for part in llm_response.content.parts:
        if part.text:
            LOGGER.info("[response from %s] %s", callback_context.agent_name, part.text)
        elif part.function_call:
            LOGGER.info(
                "[function call from %s] %s",
                callback_context.agent_name,
                part.function_call.name,
            )
    return None

