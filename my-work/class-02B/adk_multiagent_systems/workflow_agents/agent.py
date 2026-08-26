"""Class 02B starter: a working sequential workflow to extend in Tasks 5-6."""

from __future__ import annotations

import logging
import re
from pathlib import Path

from google.adk.agents import Agent, LoopAgent, ParallelAgent, SequentialAgent
from google.adk.apps import App
from google.adk.integrations.langchain import LangchainTool
from google.adk.models import Gemini
from google.adk.tools.tool_context import ToolContext
from google.genai import types
import wikipedia
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

wikipedia.set_user_agent("MoviePitchAgent/1.0 (agent_engineering_lab)")

from adk_multiagent_systems.shared import (
    MODEL_NAME,
    PROJECT_ROOT,
    RETRY_OPTIONS,
    Graceful429Plugin,
    log_model_response,
    log_query_to_model,
)

# TODO 5A: Import exit_loop here. See Task 5 in README.md.
from google.adk.tools import exit_loop

LOGGER = logging.getLogger(__name__)
OUTPUT_DIR = PROJECT_ROOT / "movie_pitches"


def build_model() -> Gemini:
    """Create the model wrapper used by each LLM agent."""
    return Gemini(model=MODEL_NAME, retry_options=RETRY_OPTIONS)


# Tools

def append_to_state(
    tool_context: ToolContext,
    field: str,
    response: str,
) -> dict[str, str]:
    """Append new output to a list stored under a session-state key."""
    existing_state = tool_context.state.get(field, [])
    if not isinstance(existing_state, list):
        existing_state = [str(existing_state)]
    tool_context.state[field] = [*existing_state, response]
    LOGGER.info("Added an item to state key %s", field)
    return {"status": "success"}


def write_file(
    tool_context: ToolContext,
    directory: str,
    filename: str,
    content: str,
) -> dict[str, str]:
    """Safely write a text file inside the fixed movie_pitches directory."""
    del tool_context, directory
    safe_stem = re.sub(r"[^A-Za-z0-9._-]+", "_", Path(filename).stem).strip("._")
    safe_stem = safe_stem or "movie_pitch"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    target = OUTPUT_DIR / f"{safe_stem}.txt"
    target.write_text(content, encoding="utf-8")
    return {
        "status": "success",
        "path": str(target.relative_to(PROJECT_ROOT)),
    }


# Agents
# TODO 5B: Add critic under this header.
critic = Agent(
    name="critic",
    model=build_model(),
    description="Reviews the outline so that it can be improved.",
    instruction="""
    INSTRUCTIONS:
    Consider these questions about the PLOT_OUTLINE:
    - Does it have a satisfying three-act cinematic structure?
    - Are the characters' struggles engaging?
    - Does it feel grounded in a real historical period?
    - Does it incorporate useful historical details from RESEARCH?

    If the PLOT_OUTLINE does a good job on these questions, call exit_loop.
    If significant improvements can be made, call append_to_state with field
    'CRITICAL_FEEDBACK' and add precise feedback for the next pass.
    Explain your decision and briefly summarize the feedback provided.

    PLOT_OUTLINE:
    { PLOT_OUTLINE? }

    RESEARCH:
    { research? }
    """,
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
    tools=[append_to_state, exit_loop],
)

# TODO 6A: Later add the two report agents and ParallelAgent under this header.

file_writer = Agent(
    name="file_writer",
    model=build_model(),
    description="Creates marketing details and saves a pitch document.",
    instruction="""
    INSTRUCTIONS:
    - Create a marketable, contemporary movie title suggestion for the movie
      described in the PLOT_OUTLINE. If a title has been suggested in
      PLOT_OUTLINE, you can use it, or replace it with a better one.
    - Use your 'write_file' tool to create a new txt file with these arguments:
        - For filename, use the movie title.
        - Write to the 'movie_pitches' directory.
        - For content, extract from PLOT_OUTLINE:
            - A logline
            - A synopsis or plot outline

    PLOT_OUTLINE:
    { PLOT_OUTLINE? }

    # TODO 6C: Replace this entire instruction with the report-aware version.
    """,
    generate_content_config=types.GenerateContentConfig(temperature=0),
    tools=[write_file],
)

screenwriter = Agent(
    name="screenwriter",
    model=build_model(),
    description=(
        "Write a logline and plot outline for a biopic about a historical "
        "character."
    ),
    instruction="""
    INSTRUCTIONS:
    Your goal is to write a logline and three-act plot outline for an inspiring
    movie about the historical character(s) described by PROMPT: { PROMPT? }

    - If there is CRITICAL_FEEDBACK, use it to improve the outline.
    - If there is RESEARCH, use relevant historical details.
    - If there is a PLOT_OUTLINE, improve upon it.
    - Use append_to_state to write the new draft to 'PLOT_OUTLINE'.
    - Summarize what you focused on in this pass.

    PLOT_OUTLINE:
    { PLOT_OUTLINE? }

    RESEARCH:
    { research? }

    CRITICAL_FEEDBACK:
    { CRITICAL_FEEDBACK? }
    """,
    generate_content_config=types.GenerateContentConfig(temperature=0),
    tools=[append_to_state],
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
)

researcher = Agent(
    name="researcher",
    model=build_model(),
    description="Answer research questions using Wikipedia.",
    instruction="""
    PROMPT:
    { PROMPT? }

    PLOT_OUTLINE:
    { PLOT_OUTLINE? }

    CRITICAL_FEEDBACK:
    { CRITICAL_FEEDBACK? }

    INSTRUCTIONS:
    - If there is CRITICAL_FEEDBACK, research facts that address it.
    - If there is PLOT_OUTLINE, research facts that add historical detail.
    - If both are empty, gather facts about the person in PROMPT.
    - Use append_to_state to add your research to 'research'.
    - Summarize what you learned.
    """,
    generate_content_config=types.GenerateContentConfig(temperature=0),
    tools=[
        LangchainTool(
            tool=WikipediaQueryRun(
                api_wrapper=WikipediaAPIWrapper(),
                handle_tool_error=True,
            )
        ),
        append_to_state,
    ],
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
)

# TODO 5C: Add writers_room above film_concept_team.
writers_room = LoopAgent(
    name="writers_room",
    description="Iterates through research and writing to improve a movie plot outline.",
    sub_agents=[researcher, screenwriter, critic],
    max_iterations=5,
)

film_concept_team = SequentialAgent(
    name="film_concept_team",
    description="Write a film plot outline and save it as a text file.",
    # sub_agents=[researcher, screenwriter, file_writer],
    # TODO 5D: Replace the list above with [writers_room, file_writer].
    sub_agents=[writers_room, file_writer],
    # TODO 6B: Later replace it with
    #           [writers_room, preproduction_team, file_writer].
)

root_agent = Agent(
    name="greeter",
    model=build_model(),
    description="Guides the user in crafting a movie plot.",
    instruction="""
    - Tell the user you will help write a pitch for a hit movie. Ask for a
      historical figure to create a movie about.
    - When the user responds, use append_to_state to store the response in
      'PROMPT', then transfer to film_concept_team.
    """,
    generate_content_config=types.GenerateContentConfig(temperature=0),
    tools=[append_to_state],
    sub_agents=[film_concept_team],
)

quota_plugin = Graceful429Plugin(
    name="graceful_429_plugin",
    fallback_text={
        "default": (
            "The model quota is temporarily exhausted. Your session state is "
            "preserved; wait briefly and retry the last step."
        )
    },
)

app = App(
    name="workflow_agents",
    root_agent=root_agent,
    plugins=[quota_plugin],
)
