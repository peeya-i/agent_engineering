"""Class 02C golden application: parent, sub-agent, peer transfer, and session state."""

from __future__ import annotations

from typing import List

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.adk.tools.tool_context import ToolContext
from google.genai import types

from adk_multiagent_systems.shared import (
    MODEL_NAME,
    RETRY_OPTIONS,
    Graceful429Plugin,
    log_model_response,
    log_query_to_model,
)


def build_model() -> Gemini:
    """Create the model wrapper used by each LLM agent."""
    return Gemini(model=MODEL_NAME, retry_options=RETRY_OPTIONS)


# Tools

def save_attractions_to_state(
    tool_context: ToolContext,
    attractions: List[str],
) -> dict[str, str]:
    """Save new attractions in the session state's attractions list."""
    existing_attractions = tool_context.state.get("attractions", [])
    tool_context.state["attractions"] = existing_attractions + attractions
    return {"status": "success"}


# Agents

attractions_planner = Agent(
    name="attractions_planner",
    model=build_model(),
    description="Build a list of attractions to visit in a country.",
    instruction="""
        - Provide the user options for attractions to visit within their
          selected country.

        - When the user replies, use your tool to save their selected
          attraction, and then provide more possible attractions.
        - If they ask to view the list, provide a bulleted list of
          {attractions?} and then suggest some more.
        """,
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
    tools=[save_attractions_to_state],
)

travel_brainstormer = Agent(
    name="travel_brainstormer",
    model=build_model(),
    description="Help a user decide what country to visit.",
    instruction="""
        Provide a few suggestions of popular countries for travelers.

        Help a user identify their primary goals of travel:
        adventure, leisure, learning, shopping, or viewing art.

        Identify countries that would make great destinations
        based on their priorities.
        """,
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
)

root_agent = Agent(
    name="steering",
    model=build_model(),
    description="Start a user on a travel adventure.",
    instruction="""
        Ask the user if they know where they'd like to travel
        or if they need some help deciding.

        If they need help deciding, send them to 'travel_brainstormer'.
        If they know what country they'd like to visit, send them to
        'attractions_planner'.
        """,
    generate_content_config=types.GenerateContentConfig(temperature=0),
    sub_agents=[travel_brainstormer, attractions_planner],
)

quota_plugin = Graceful429Plugin(
    name="graceful_429_plugin",
    fallback_text={
        "default": (
            "The model quota is temporarily exhausted. Wait briefly, then "
            "retry the last travel request."
        )
    },
)

app = App(
    name="parent_and_subagents",
    root_agent=root_agent,
    plugins=[quota_plugin],
)
