"""
Multi-Skill Agent — Code Review & Unit Test Generation

This agent demonstrates a multi-skill architecture using Google ADK.
A root agent routes user requests to specialized sub-agents:
  - code_review_agent: Reviews code for issues, best practices, and improvements.
  - unit_test_agent: Generates unit test stubs for functions and methods.

Each sub-agent has its own placeholder tools that demonstrate the pattern.
The tools don't perform real analysis yet — they return structured placeholder
responses to show how the skill pipeline would work.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.agents.context_cache_config import ContextCacheConfig
from google.adk.apps.app import App
from google.adk.sessions import DatabaseSessionService

load_dotenv()

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# =============================================================================
# SESSION PERSISTENCE — SQLite at .adk/session.db
# =============================================================================

DB_DIR = Path(__file__).parent.parent / ".adk"
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_URL = f"sqlite+aiosqlite:///{DB_DIR / 'session.db'}"

session_service = DatabaseSessionService(db_url=DB_URL)

import sys

# Add skill scripts directories to sys.path to load tool functions dynamically
sys.path.append(str(Path(__file__).parent.parent / "skills/code-review/scripts"))
sys.path.append(str(Path(__file__).parent.parent / "skills/unit-test-generator/scripts"))

from review_code import review_code
from summarize_review import summarize_review
from generate_unit_tests import generate_unit_tests
from summarize_tests import summarize_tests


# =============================================================================
# SUB-AGENT 1: Code Review Agent
# =============================================================================

code_review_agent = Agent(
    name="code_review_agent",
    model=GEMINI_MODEL,
    description=(
        "Specialized agent for code review. Delegates to this agent when "
        "the user wants to review code, check for issues, get best practice "
        "suggestions, or analyze code quality."
    ),
    instruction=(
        "You are a Code Review specialist. Your job is to help users review "
        "their code for issues, best practices, and potential improvements.\n\n"
        "WORKFLOW — follow these steps and summarize each one:\n"
        "1. RECEIVE: Accept the code from the user. Acknowledge what you received.\n"
        "2. REVIEW: Use the `review_code` tool to analyze the code.\n"
        "3. SUMMARIZE: Use the `summarize_review` tool to create an actionable summary.\n"
        "4. PRESENT: Present the findings to the user in a clear, structured format.\n\n"
        "For EACH step, provide a brief summary of what happened, like:\n"
        "  **Step 1 — Received Code**: Received a Python function `add(a, b)` (42 chars)\n"
        "  **Step 2 — Review**: Found 0 critical, 1 warning, 2 suggestions\n"
        "  **Step 3 — Summary**: Top priority is adding documentation\n\n"
        "Always be constructive and specific in your feedback."
    ),
    tools=[review_code, summarize_review],
)


# =============================================================================
# SUB-AGENT 2: Unit Test Generation Agent
# =============================================================================

unit_test_agent = Agent(
    name="unit_test_agent",
    model=GEMINI_MODEL,
    description=(
        "Specialized agent for unit test generation. Delegates to this agent "
        "when the user wants to generate unit tests, create test stubs, or "
        "get test coverage for their functions and methods."
    ),
    instruction=(
        "You are a Unit Test Generation specialist. Your job is to help users "
        "create comprehensive unit tests for their code.\n\n"
        "WORKFLOW — follow these steps and summarize each one:\n"
        "1. RECEIVE: Accept the code from the user. Identify the functions/methods to test.\n"
        "2. GENERATE: Use the `generate_unit_tests` tool to create test stubs.\n"
        "3. SUMMARIZE: Use the `summarize_tests` tool to summarize coverage.\n"
        "4. PRESENT: Present the generated tests and summary to the user.\n\n"
        "For EACH step, provide a brief summary of what happened, like:\n"
        "  **Step 1 — Received Code**: Found 2 functions to test: `multiply`, `divide`\n"
        "  **Step 2 — Generated Tests**: Created 3 test stubs covering key paths\n"
        "  **Step 3 — Summary**: ~60% estimated coverage, recommend boundary tests\n\n"
        "Always explain what each test covers and why it matters."
    ),
    tools=[generate_unit_tests, summarize_tests],
)


# =============================================================================
# ROOT AGENT: Multi-Skill Router
# =============================================================================

root_agent = Agent(
    name="multiskill_router",
    model=GEMINI_MODEL,
    description="Root agent that routes requests to specialized skill agents.",
    instruction=(
        "You are a Multi-Skill Code Assistant that helps developers with two skills:\n\n"
        "AVAILABLE SKILLS:\n"
        "1. **Code Review** — Analyze code for issues, best practices, and improvements.\n"
        "   Route to: `code_review_agent`\n"
        "2. **Unit Test Generation** — Generate unit test stubs for functions and methods.\n"
        "   Route to: `unit_test_agent`\n\n"
        "YOUR RESPONSIBILITIES:\n"
        "- Identify which skill the user needs based on their request.\n"
        "- Route the request to the appropriate sub-agent.\n"
        "- If the user's intent is unclear, ask them to clarify whether they want "
        "  a code review or unit tests.\n"
        "- If the user asks for both, handle them sequentially — review first, then tests.\n\n"
        "TURN SUMMARY:\n"
        "At the end of each turn, provide a brief summary of:\n"
        "- What skill was activated\n"
        "- What steps were taken\n"
        "- Key findings or outputs\n\n"
        "GREETING:\n"
        "When the user first connects, introduce yourself and list the available skills."
    ),
    sub_agents=[code_review_agent, unit_test_agent],
)


# =============================================================================
# APP: Wraps root_agent with context caching to avoid re-sending prompts
# on every agent transfer. adk web discovers this `app` export.
# =============================================================================

app = App(
    name="multiskill_agent",
    root_agent=root_agent,
    context_cache_config=ContextCacheConfig(
        min_tokens=0,
        ttl_seconds=1800,
        cache_intervals=10,
    ),
)
