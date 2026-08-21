# Setup

## Prerequisites

- Python 3.11 or newer
- Google Cloud project with Vertex AI enabled
- Authenticated `gcloud` session or Application Default Credentials

## 1. Create the environment

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Windows PowerShell activation:

```powershell
.venv\Scripts\Activate.ps1
```

## 2. Configure the agent

```bash
cp .env.example .env
```

Edit `.env` and set your project. Keep `renewal_desk_agent` as the ADK application directory.

## 3. Run the structural tests

```bash
pytest -q
```

The starter deliberately contains `TODO` items, so some tests should initially fail.

## 4. Launch ADK Web

Run this command from the directory containing `renewal_desk_agent/`:

```bash
adk web .
```

Open the local URL, select `renewal_desk_agent`, and start a new session for each evaluation case.

## 5. Inspect progressive loading

In ADK Web, open the event or trace view and look for:

1. `list_skills` or the L1 skill catalog
2. `load_skill` for L2
3. `load_skill_resource` for selected references/assets
4. `run_skill_script` for the deterministic calculator

Record the observed order and exact paths in `SUBMISSION.md`.

## Troubleshooting

- Skill loading fails: ensure the directory and frontmatter name are both `renewal-advisor`.
- Model not found: set `AGENT_MODEL` in `.env` to a Gemini model available in your project and region.
- Resource not found: copy the exact path from `SKILL.md`; do not guess alternate paths repeatedly.
- Script execution: this lab uses the local unsafe executor only for a reviewed, deterministic classroom script. Do not use that executor with untrusted scripts or in production.
