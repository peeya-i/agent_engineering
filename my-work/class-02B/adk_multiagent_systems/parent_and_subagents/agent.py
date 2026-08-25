"""Class 02B starter: parent, sub-agent, peer transfer, and session state."""

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
# TODO 3A: Add save_attractions_to_state here.
# The exact code is in Task 3 of README.md.


# Agents

attractions_planner = Agent(
    name="attractions_planner",
    model=build_model(),
    description="Build a list of attractions to visit in a country.",
    instruction="""
        - Provide the user options for attractions to visit within their
          selected country.

        # TODO 3C: Add the two state-aware instruction bullets here.
        """,
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
    # TODO 3B: Add tools=[save_attractions_to_state] below this line.
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

        # TODO 2B: Add the explicit transfer instructions here.
        """,
    generate_content_config=types.GenerateContentConfig(temperature=0),
    # TODO 2A: Add the sub_agents parameter below this line.
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
