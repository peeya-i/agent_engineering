"""WidgetWare Renewal Desk Agent for the progressive skills lab."""

import os
from pathlib import Path

from dotenv import load_dotenv
from google.adk import Agent
from google.adk.code_executors.unsafe_local_code_executor import (
    UnsafeLocalCodeExecutor,
)
from google.adk.skills import load_skill_from_dir
from google.adk.tools.skill_toolset import SkillToolset


load_dotenv()

SKILL_DIR = Path(__file__).parent / "skills" / "renewal-advisor"
renewal_skill = load_skill_from_dir(SKILL_DIR)

# Classroom use only. This executor runs local code and must not be used with
# untrusted skill packages or as a production isolation boundary.
skill_toolset = SkillToolset(
    skills=[renewal_skill],
    code_executor=UnsafeLocalCodeExecutor(),
)

root_agent = Agent(
    name="renewal_desk_agent",
    model=os.getenv("AGENT_MODEL", "gemini-2.5-flash"),
    description="Helps WidgetWare teams analyze enterprise renewals.",
    instruction=(
        "You are WidgetWare's Renewal Desk Agent. Use specialized skills when "
        "relevant. Treat skill resources as the only source for internal policy. "
        "Never invent approvals, policy exceptions, deadlines, control IDs, or "
        "commercial commitments. Show concise reasoning and preserve source citations."
    ),
    tools=[skill_toolset],
)
