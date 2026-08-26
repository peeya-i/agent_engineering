"""Check that every Class 02B topology checkpoint is complete.

Class 02C runs this as an acceptance gate: the observability lab needs the
finished sequential/loop/parallel topology, so every line must report PASS.
"""

from __future__ import annotations

import sys

from adk_multiagent_systems.parent_and_subagents.agent import (
    attractions_planner,
    root_agent as travel_root,
)
from adk_multiagent_systems.workflow_agents.agent import (
    film_concept_team,
)


def names(agents) -> list[str]:
    return [agent.name for agent in agents]


def tool_names(agent) -> list[str]:
    return [
        getattr(tool, "name", getattr(tool, "__name__", ""))
        for tool in getattr(agent, "tools", [])
    ]


def report(label: str, ok: bool, detail: str = "") -> bool:
    print(f"{label} {'PASS' if ok else 'TODO'}{f' {detail}' if detail else ''}")
    return ok


def main() -> None:
    results: list[bool] = []

    travel_children = names(travel_root.sub_agents)
    results.append(
        report(
            "Task 2 delegation:",
            travel_children == ["travel_brainstormer", "attractions_planner"],
            str(travel_children),
        )
    )

    results.append(
        report(
            "Task 3 session-state tool:",
            "save_attractions_to_state" in tool_names(attractions_planner),
        )
    )

    sequence = names(film_concept_team.sub_agents)
    results.append(
        report(
            "Task 4 sequential baseline:",
            sequence == ["writers_room", "preproduction_team", "file_writer"],
            str(sequence),
        )
    )

    loop = next(
        (a for a in film_concept_team.sub_agents if a.name == "writers_room"),
        None,
    )
    loop_children = names(loop.sub_agents) if loop else []
    critic = next((a for a in (loop.sub_agents if loop else []) if a.name == "critic"), None)
    results.append(
        report(
            "Task 5 loop:",
            loop is not None
            and loop_children == ["researcher", "screenwriter", "critic"]
            and getattr(loop, "max_iterations", None) == 5
            and "exit_loop" in tool_names(critic),
            str(loop_children),
        )
    )

    parallel = next(
        (a for a in film_concept_team.sub_agents if a.name == "preproduction_team"),
        None,
    )
    branches = names(parallel.sub_agents) if parallel else []
    output_keys = sorted(
        getattr(a, "output_key", None) or "" for a in (parallel.sub_agents if parallel else [])
    )
    results.append(
        report(
            "Task 6 parallel fan-out/gather:",
            parallel is not None
            and branches == ["box_office_researcher", "casting_agent"]
            and output_keys == ["box_office_report", "casting_report"],
            str(branches),
        )
    )

    if all(results):
        print("All checkpoints PASS. This is the completed golden application.")
    else:
        print("Incomplete source. Class 02C requires the completed golden application.")
        sys.exit(1)


if __name__ == "__main__":
    main()
