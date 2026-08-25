# Multi-Skill ADK Agent — Code Review & Unit Test Generation

A Google ADK agent demonstrating multi-skill architecture with two specialized
sub-agents: **Code Review** and **Unit Test Generation**.

## Architecture

```
┌─────────────────────────────────────────────┐
│           root_agent (Router)               │
│  Identifies user intent and delegates to    │
│  the appropriate specialized sub-agent      │
└──────────┬─────────────────┬────────────────┘
           │                 │
    ┌──────▼──────┐   ┌─────▼───────────┐
    │ code_review │   │  unit_test      │
    │ _agent      │   │  _agent         │
    │             │   │                 │
    │ Tools:      │   │ Tools:          │
    │ • review_   │   │ • generate_     │
    │   code      │   │   unit_tests    │
    │ • summarize │   │ • summarize_    │
    │   _review   │   │   tests         │
    └─────────────┘   └─────────────────┘
```

## Project Structure

```
class-02-multiskills/
├── multiskill_agent/          # ADK agent package
│   ├── __init__.py            # Package init
│   ├── agent.py               # Root + sub-agents + tools
│   └── .env                   # API key config
├── skills/                    # Skill definitions
│   ├── code-review/
│   │   └── SKILL.md           # Code review skill spec
│   └── unit-test-generator/
│       └── SKILL.md           # Unit test skill spec
└── README.md                  # This file
```

## Setup

### 1. Install Google ADK

```bash
pip install google-adk
```

### 2. Configure API Key

Edit `multiskill_agent/.env` and set your Gemini API key:

```
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your-actual-api-key
```

Get an API key from [Google AI Studio](https://aistudio.google.com/app/api-keys).

### 3. Run the Agent

From this directory (`class-02-multiskills`):

```bash
cd class-02-multiskills
source .venv/bin/activate
adk web . --port 8001
```

Then open [http://localhost:8001](http://localhost:8001) in your browser.

## Usage

1. Open the ADK Dev UI at `http://localhost:8001`
2. Select **multiskill_agent** from the agent dropdown
3. Try these example prompts:

| Skill | Example Prompt |
|-------|---------------|
| Code Review | "Review this code: `def add(a, b): return a + b`" |
| Unit Tests | "Generate unit tests for: `def multiply(x, y): return x * y`" |
| Both | "Review and write tests for this function: `def divide(a, b): return a / b`" |

## How It Works

1. **Root Agent** receives the user message and identifies intent
2. **Routes** to the appropriate sub-agent (`code_review_agent` or `unit_test_agent`)
3. **Sub-agent** executes its workflow using placeholder tools
4. **Each step is summarized** so the user can follow the agent's reasoning
5. **Final response** includes a structured summary of findings

> **Note**: All tools are placeholders returning demo data. The structure
> demonstrates how a real multi-skill agent would be organized.
