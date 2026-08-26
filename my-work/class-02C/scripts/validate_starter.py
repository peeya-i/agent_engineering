"""Validate the completed golden package without making a model API call."""

from __future__ import annotations

import asyncio

import google.adk

from adk_multiagent_systems.parent_and_subagents.agent import app as travel_app
from adk_multiagent_systems.shared.plugins import Graceful429Plugin
from adk_multiagent_systems.workflow_agents.agent import app as workflow_app


async def validate_plugin() -> None:
    plugin = Graceful429Plugin(
        name="validation_plugin",
        fallback_text="Validation fallback",
    )
    response = await plugin.on_model_error_callback(
        callback_context=None,
        llm_request="validation request",
        error=Exception("429 RESOURCE_EXHAUSTED"),
    )
    assert response is not None
    assert response.content.parts[0].text == "Validation fallback"


def main() -> None:
    assert travel_app.root_agent.name == "steering"
    assert workflow_app.root_agent.name == "greeter"
    assert [agent.name for agent in workflow_app.root_agent.sub_agents] == [
        "film_concept_team"
    ]
    asyncio.run(validate_plugin())
    print(f"google-adk: {google.adk.__version__}")
    print("Golden package imports: OK")
    print("Workflow topology reachable: OK")
    print("Validation passed. No model API call was made.")


if __name__ == "__main__":
    main()
