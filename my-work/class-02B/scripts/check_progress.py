"""Check which Class 02B topology checkpoints have been completed."""

from __future__ import annotations

from adk_multiagent_systems.parent_and_subagents.agent import (
    attractions_planner,
    root_agent as travel_root,
)
from adk_multiagent_systems.workflow_agents.agent import (
    film_concept_team,
)


def names(agents) -> list[str]:
    return [agent.name for agent in agents]


def main() -> None:
    travel_children = names(travel_root.sub_agents)
    print(
        "Task 2 delegation:",
        "PASS" if travel_children == ["travel_brainstormer", "attractions_planner"] else "TODO",
    )

    tool_names = [getattr(tool, "name", getattr(tool, "__name__", "")) for tool in attractions_planner.tools]
    print(
        "Task 3 session-state tool:",
        "PASS" if "save_attractions_to_state" in tool_names else "TODO",
    )

    sequence = names(film_concept_team.sub_agents)
    print("Task 4 sequential baseline:", "PASS" if sequence else "TODO", sequence)

    loop = next((agent for agent in film_concept_team.sub_agents if agent.name == "writers_room"), None)
    print("Task 5 loop:", "PASS" if loop else "TODO")

    parallel = next(
        (agent for agent in film_concept_team.sub_agents if agent.name == "preproduction_team"),
        None,
    )
    print("Task 6 parallel fan-out/gather:", "PASS" if parallel else "TODO")


if __name__ == "__main__":
    main()
