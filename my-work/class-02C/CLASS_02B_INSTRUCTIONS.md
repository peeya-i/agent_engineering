# Class 02B - Build Multi-Agent Systems with ADK 2.x

> **Class 02C package note:** The complete Class 02B code is already extracted into the `class-02C/` directory. Skip Class 02B Task 1.1 (`unzip class-02B.zip` and `cd class-02B`). Run the remaining setup and build tasks from the `class-02C/` root.

This is a **student starter**, not a finished solution. The supplied code runs at useful checkpoints, but the lines marked `TODO 2A` through `TODO 6C` are intentionally incomplete. You will add or modify the code yourself so you can see where orchestration behavior lives and observe the effect of each change.

The progression follows the supplied Google Skills lab:

1. Set up ADK locally.
2. Connect a parent to specialist sub-agents.
3. store and retrieve session state.
4. Run the provided sequential workflow.
5. Add an iterative loop.
6. Add parallel fan-out and gather.

The learning code follows the PDF's agent names, state keys, and task order. Infrastructure-only details have been updated for Google ADK 2.x: current imports, current plugin callbacks, one project-level `.env`, and local-safe logging.

## What is deliberately incomplete

| File | Starting point | Student work |
|---|---|---|
| `parent_and_subagents/agent.py` | Three LLM agents exist but are not connected; no state tool exists | Add delegation, explicit routing, a state-writing tool, and state-aware instructions |
| `workflow_agents/agent.py` | A working `SequentialAgent` performs research -> writing -> file output | Add `LoopAgent`, critic, `ParallelAgent`, two reporting agents, and gathered final output |
| `shared/` | Complete ADK 2.x runtime support | Do not modify for this lab |

## Task 1 - Expand, install, and authenticate

### 1.1 Expand the ZIP

```bash
unzip class-02B.zip
cd class-02B
```

You should now see:

```text
class-02B/
├── .env.api-key.example
├── .env.vertex.example
├── README.md
├── pyproject.toml
├── adk_multiagent_systems/
│   ├── parent_and_subagents/agent.py
│   ├── shared/
│   └── workflow_agents/agent.py
├── movie_pitches/
└── scripts/
```

### 1.2 Create an isolated Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 1.3 Install ADK 2.x and the starter

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

This installs `google-adk[gcp]==2.6.0`, the current ADK 2.x version used by this package, along with the Wikipedia/LangChain dependencies.

Verify:

```bash
python -c "import google.adk; print(google.adk.__version__)"
python scripts/validate_starter.py
```

Expected final lines:

```text
Starter imports: OK
Sequential baseline: OK
Validation passed. No model API call was made.
```

### 1.4 Choose one authentication method

Use **one** option. Both create the same root file, `.env`.

#### Option A - Gemini API key

```bash
cp .env.api-key.example .env
```

Edit `.env`:

```dotenv
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=replace_with_your_google_ai_studio_key
MODEL=gemini-2.5-flash
```

**Why:** `FALSE` tells the Google Gen AI SDK to authenticate with a Gemini API key.

**Impact:** model calls go through the Gemini Developer API and do not require `gcloud` Application Default Credentials.

#### Option B - Vertex AI

```bash
cp .env.vertex.example .env
```

Edit `.env`:

```dotenv
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=your_project_id
GOOGLE_CLOUD_LOCATION=global
MODEL=gemini-2.5-flash
```

Then authenticate:

```bash
gcloud auth application-default login
gcloud services enable aiplatform.googleapis.com --project=your_project_id
```

**Why:** `TRUE` selects Vertex AI and associates requests with your Google Cloud project and location.

**Impact:** model calls use Google Cloud authentication, IAM, quotas, and project billing.

Do not use `VERTEX_AI=true` or `vertex_Ai=true`; the recognized variable is exactly `GOOGLE_GENAI_USE_VERTEXAI=TRUE`.

## Task 2 - Connect the parent and specialist agents

Open:

```text
adk_multiagent_systems/parent_and_subagents/agent.py
```

The file already defines:

- `steering` - the root/parent agent;
- `travel_brainstormer` - helps choose a destination; and
- `attractions_planner` - suggests attractions for a known country.

At the start, the objects exist but the parent has no `sub_agents`, so ADK has no delegation tree.

### 2A - Add the parent-child relationship

Find `TODO 2A` inside `root_agent = Agent(...)`. Replace the TODO comment with:

```python
sub_agents=[travel_brainstormer, attractions_planner],
```

The end of `root_agent` should now look like:

```python
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
    sub_agents=[travel_brainstormer, attractions_planner],
)
```

**Why here:** the hierarchy is declared on the parent; sub-agents do not need a separate `parent` parameter.

**Impact:** ADK can now transfer the conversation from `steering` to either specialist based on each specialist's `description`.

Run it:

```bash
cd adk_multiagent_systems
adk run parent_and_subagents
```

Try:

```text
hello
I could use some help deciding.
```

Observe the responding agent name. You should see a transfer from `[steering]` to `[travel_brainstormer]`.

Enter `exit`, then return to the project root:

```bash
cd ..
```

### 2B - Make routing intent explicit

Find `TODO 2B` inside the root agent's triple-quoted `instruction`. Replace only that TODO line with:

```text
        If they need help deciding, send them to 'travel_brainstormer'.
        If they know what country they'd like to visit, send them to
        'attractions_planner'.
```

**Why here:** descriptions make delegation possible; the root instruction makes the routing policy explicit.

**Impact:** prompts such as “I would like to go to Japan” route more predictably to `attractions_planner`, while uncertainty routes to `travel_brainstormer`.

Run again:

```bash
cd adk_multiagent_systems
adk run parent_and_subagents
```

Test both directions:

```text
I would like to go to Japan.
Actually, I do not know what country to visit.
```

The second request can transfer between peer agents because both specialists share the same parent.

## Task 3 - Store and retrieve session state

Return to:

```text
adk_multiagent_systems/parent_and_subagents/agent.py
```

### 3A - Add the state-writing tool

Find `TODO 3A` under `# Tools`. Replace the two TODO comment lines with:

```python
def save_attractions_to_state(
    tool_context: ToolContext,
    attractions: List[str],
) -> dict[str, str]:
    """Save new attractions in the session state's attractions list."""
    existing_attractions = tool_context.state.get("attractions", [])
    tool_context.state["attractions"] = existing_attractions + attractions
    return {"status": "success"}
```

**Why here:** tools are regular Python functions defined before the agents that use them. ADK injects `ToolContext` when the model calls the function.

**Impact:** changing `tool_context.state` produces a state delta event and makes the updated list available to every agent in the same session.

### 3B - Give the planner access to the tool

Find `TODO 3B` inside `attractions_planner = Agent(...)`. Replace the TODO with:

```python
tools=[save_attractions_to_state],
```

**Why here:** defining a function does not expose it to an agent. The `tools` list defines the planner's allowed actions.

**Impact:** `attractions_planner` can now choose to persist selected attractions; the other agents cannot call this tool directly.

### 3C - Tell the planner when to write and read state

Find `TODO 3C` inside `attractions_planner`'s instruction. Replace it with:

```text
        - When the user replies, use your tool to save their selected
          attraction, and then provide more possible attractions.
        - If they ask to view the list, provide a bulleted list of
          {attractions?} and then suggest some more.
```

**Why here:** the tool grants capability; the instruction establishes when to use it. `{attractions?}` injects the current state value, and `?` makes the key optional before it exists.

**Impact:** selections persist across turns, and “What is on my list?” can be answered from structured state rather than only conversation history.

### 3D - Inspect the state delta in ADK Web

From `class-02B/adk_multiagent_systems`:

```bash
adk web --port 8000 --reload_agents
```

Open `http://127.0.0.1:8000`, select `parent_and_subagents`, and try:

```text
hello
I'd like to go to Egypt.
I'll go to the Sphinx.
What is on my list?
```

Inspect:

- the tool event and its `state_delta`;
- the State tab's `attractions` array; and
- the final response generated using `{attractions?}`.

Stop with `Ctrl+C`. From the project root, check progress:

```bash
python scripts/check_progress.py
```

Tasks 2 and 3 should show `PASS`.

## Task 4 - Run the provided SequentialAgent baseline

Open:

```text
adk_multiagent_systems/workflow_agents/agent.py
```

Task 4 is intentionally prebuilt so you begin with a working comparison point. The baseline contains:

```python
film_concept_team = SequentialAgent(
    name="film_concept_team",
    description="Write a film plot outline and save it as a text file.",
    sub_agents=[researcher, screenwriter, file_writer],
)
```

**Why this order:** research must exist before drafting, and the completed draft must exist before file output.

**Impact:** after the user chooses a subject, ADK executes the three sub-agents automatically in a deterministic order without waiting for another user turn between stages.

Run from `class-02B/adk_multiagent_systems`:

```bash
adk web --port 8000 --reload_agents
```

Select `workflow_agents`, enter `hello`, then try:

```text
Ada Lovelace
```

Inspect the event graph and the generated file under:

```text
class-02B/movie_pitches/
```

This is your baseline. Stop the server before Task 5, or leave `--reload_agents` running and create a new session after each code change.

## Task 5 - Add iterative refinement with LoopAgent

You will change the movie workflow from:

```text
researcher -> screenwriter -> file_writer
```

to:

```text
(researcher -> screenwriter -> critic) repeated -> file_writer
```

### 5A - Import the loop-exit tool

Find `TODO 5A` near the imports. Replace it with:

```python
from google.adk.tools import exit_loop
```

**Why here:** `LoopAgent` repeats until its maximum is reached unless a child invokes an explicit exit mechanism.

**Impact:** the critic will be able to stop the loop early when the draft is good enough.

### 5B - Add the critic agent

Find `TODO 5B` under `# Agents`. Replace that TODO line with:

```python
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
```

Leave the nearby `TODO 6A` comment for the next task.

**Why here:** the critic is an LLM agent with two bounded choices: write structured feedback into state or call `exit_loop`.

**Impact:** each loop pass becomes evaluative. Weak drafts create `CRITICAL_FEEDBACK`; strong drafts terminate without consuming every allowed iteration.

### 5C - Wrap research, writing, and critique in a loop

Find `TODO 5C` immediately above `film_concept_team`. Replace it with:

```python
writers_room = LoopAgent(
    name="writers_room",
    description="Iterates through research and writing to improve a movie plot outline.",
    sub_agents=[researcher, screenwriter, critic],
    max_iterations=5,
)
```

**Why here:** Python objects must exist before they can be referenced in a parent's `sub_agents` list.

**Impact:** one `writers_room` execution can perform up to five research-write-critique passes. `max_iterations` is a safety bound even though `exit_loop` can stop it sooner.

### 5D - Put the loop into the sequential workflow

In `film_concept_team`, replace:

```python
sub_agents=[researcher, screenwriter, file_writer],
```

with:

```python
sub_agents=[writers_room, file_writer],
```

Remove the completed `TODO 5D` comment. Keep `TODO 6B` for the next task.

**Why here:** the sequential parent should treat the entire writing loop as one stage, then move to file output after the loop ends.

**Impact:** the file is written only after iterative refinement completes.

Test in a **new ADK session**:

```text
an industrial designer who made products for the masses
```

Observe repeated `researcher`, `screenwriter`, and `critic` events. Inspect `PLOT_OUTLINE`, `research`, and `CRITICAL_FEEDBACK` in State.

## Task 6 - Add parallel fan-out and gather

You will extend the post-writing sequence to:

```text
writers_room -> (box-office research || casting) -> file_writer
```

### 6A - Add two independent agents and a ParallelAgent

Find `TODO 6A` under `# Agents`. Replace the TODO line with:

```python
box_office_researcher = Agent(
    name="box_office_researcher",
    model=build_model(),
    description="Considers the box-office potential of this film.",
    instruction="""
    PLOT_OUTLINE:
    { PLOT_OUTLINE? }

    INSTRUCTIONS:
    Write a report on the box-office potential of a movie like the one in
    PLOT_OUTLINE, using the reported performance of comparable recent films.
    """,
    output_key="box_office_report",
)

casting_agent = Agent(
    name="casting_agent",
    model=build_model(),
    description="Generates casting ideas for this film.",
    instruction="""
    PLOT_OUTLINE:
    { PLOT_OUTLINE? }

    INSTRUCTIONS:
    Generate casting ideas for the characters in PLOT_OUTLINE. Suggest actors
    who have received positive feedback in similar roles, and explain the fit.
    """,
    output_key="casting_report",
)

preproduction_team = ParallelAgent(
    name="preproduction_team",
    sub_agents=[box_office_researcher, casting_agent],
)
```

**Why here:** both report agents depend on the completed plot, but neither depends on the other. Each writes its entire response to a distinct state key through `output_key`.

**Impact:** ADK fans out to both branches concurrently. When both finish, the workflow can gather `box_office_report` and `casting_report` from state.

### 6B - Insert the parallel stage into the sequence

In `film_concept_team`, replace:

```python
sub_agents=[writers_room, file_writer],
```

with:

```python
sub_agents=[writers_room, preproduction_team, file_writer],
```

Remove the completed `TODO 6B` comment.

**Why here:** the order creates a join barrier: the file writer begins only after the parallel team has completed both branches.

**Impact:** the final stage sees the plot plus both supplemental reports.

### 6C - Gather the branch outputs in the file writer

In `file_writer`, replace its entire existing `instruction="""..."""` block, including `TODO 6C`, with:

```python
instruction="""
INSTRUCTIONS:
- Create a marketable, contemporary movie title for the movie described in
  PLOT_OUTLINE. Reuse an existing title only if it is strong.
- Use write_file to create a new txt file:
    - Use the movie title as filename.
    - Write to the movie_pitches directory.
    - Include the PLOT_OUTLINE, BOX_OFFICE_REPORT, and CASTING_REPORT.

PLOT_OUTLINE:
{ PLOT_OUTLINE? }

BOX_OFFICE_REPORT:
{ box_office_report? }

CASTING_REPORT:
{ casting_report? }
""",
```

**Why here:** parallel branches do not directly pass messages to one another. Their `output_key` values provide stable state fields for the later gather step.

**Impact:** the final file combines the creative draft, market analysis, and casting ideas rather than discarding the parallel work.

Test in a **new ADK session**:

```text
that actress who invented technology used in Wi-Fi
```

Inspect:

- two parallel branches in the event graph;
- `box_office_report` and `casting_report` in State; and
- the completed file under `class-02B/movie_pitches/`.

Then run:

```bash
cd ..
python scripts/check_progress.py
```

All tasks should show `PASS`.

## Final architecture

```text
greeter
└── film_concept_team (SequentialAgent)
    ├── writers_room (LoopAgent, max 5)
    │   ├── researcher
    │   ├── screenwriter
    │   └── critic -> exit_loop when ready
    ├── preproduction_team (ParallelAgent)
    │   ├── box_office_researcher -> state["box_office_report"]
    │   └── casting_agent -> state["casting_report"]
    └── file_writer -> movie_pitches/<title>.txt
```

## Common problems

### `ModuleNotFoundError`

Activate `.venv`, return to `class-02B`, and reinstall:

```bash
source .venv/bin/activate
python -m pip install -e .
```

### `adk: command not found`

Confirm the active executable paths:

```bash
which python
which adk
```

### API-key mode asks for Google Cloud credentials

Confirm `.env` contains:

```dotenv
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your_real_key
```

### Vertex AI returns permission or credential errors

```bash
gcloud auth application-default login
gcloud config set project your_project_id
```

Confirm your identity has permission to use Vertex AI.

### A code edit does not appear in ADK Web

Use `--reload_agents`, save the Python file, and click **+ New Session**. State and topology from an existing session can make a new build appear unchanged.

### `NameError: exit_loop is not defined`

Complete Task 5A before Task 5B:

```python
from google.adk.tools import exit_loop
```

### `NameError` for `writers_room` or `preproduction_team`

Define the object above `film_concept_team` before adding it to the sequence's `sub_agents` list.

### Indentation or syntax errors after pasting

Run:

```bash
python -m compileall -q adk_multiagent_systems
```

Then inspect the first file and line number printed by Python.

## Learning checklist

- [ ] I can explain why `description` helps an LLM parent choose a child.
- [ ] I can distinguish tool capability from instruction policy.
- [ ] I can show a `state_delta` created by a tool.
- [ ] I can explain `{key?}` state templating.
- [ ] I can distinguish LLM transfer from deterministic sequence.
- [ ] I can explain why loops need both an exit condition and a hard cap.
- [ ] I can identify work that is safe to run in parallel.
- [ ] I can explain how `output_key` enables a later gather stage.

## Source alignment note

The task order and learning edits are based on the supplied PDF, **Build Multi-Agent Systems with ADK | Google Skills**, last updated and tested July 26, 2026. The PDF used ADK 1.30.0 and older import paths. This package retains its learning sequence while using ADK 2.x-compatible imports and plugin behavior.
