"""WidgetWare Renewal Desk agent for the Class 02A skills lab."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from google.adk import Agent
from google.adk.code_executors.unsafe_local_code_executor import (
    UnsafeLocalCodeExecutor,
)
from google.adk.skills import load_skill_from_dir
from google.adk.tools.skill_toolset import SkillToolset


AGENT_DIR = Path(__file__).resolve().parent
load_dotenv(AGENT_DIR / ".env")

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.7-flash")

renewal_skill = load_skill_from_dir(
    AGENT_DIR / "skills" / "renewal-advisor"
)

# Local lab only. Do not use UnsafeLocalCodeExecutor in production.
skill_toolset = SkillToolset(
    skills=[renewal_skill],
    code_executor=UnsafeLocalCodeExecutor(),
)

root_agent = Agent(
    name="renewal_desk_agent",
    model=MODEL,
    description=(
        "WidgetWare customer-success assistant for renewal analysis. "
        "Uses specialized skills when renewal-policy expertise is needed."
    ),
    instruction=(
        "Help WidgetWare customer-success managers with renewal work. "
        "When a specialized skill is relevant, use the skill tools and follow "
        "the loaded skill instructions. Never invent internal policy or customer "
        "facts. Treat requested, routed, and approved as distinct states."
    ),
    tools=[skill_toolset],
)
