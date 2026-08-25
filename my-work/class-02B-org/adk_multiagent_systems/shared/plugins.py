"""ADK 2.x plugins shared by both examples."""

from __future__ import annotations

import logging

from google.adk.models import LlmResponse
from google.adk.plugins import BasePlugin
from google.genai import types

LOGGER = logging.getLogger(__name__)


class Graceful429Plugin(BasePlugin):
    """Return a friendly response when a model request exhausts its quota."""

    def __init__(self, name: str, fallback_text: str | dict[str, str]):
        super().__init__(name=name)
        self.fallback_text = fallback_text

    def _select_fallback(self, request: object) -> str:
        if isinstance(self.fallback_text, str):
            return self.fallback_text

        request_text = str(request).lower()
        best_match: tuple[int, str] | None = None
        for keyword, response in self.fallback_text.items():
            if keyword == "default":
                continue
            position = request_text.rfind(keyword.lower())
            if position >= 0 and (best_match is None or position > best_match[0]):
                best_match = (position, response)

        if best_match:
            return best_match[1]
        return self.fallback_text.get(
            "default",
            "The model quota is temporarily exhausted. Please try again later.",
        )

    async def on_model_error_callback(
        self,
        *,
        callback_context,
        llm_request,
        error: Exception,
    ) -> LlmResponse | None:
        """Handle model-level 429/RESOURCE_EXHAUSTED errors using the ADK 2.x hook."""
        error_text = str(error)
        if "429" not in error_text and "RESOURCE_EXHAUSTED" not in error_text:
            return None

        LOGGER.warning("Model quota exhausted in plugin %s", self.name)
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[
                    types.Part.from_text(
                        text=self._select_fallback(llm_request),
                    )
                ],
            )
        )

