# Class 02C — Observe, Record, Play, and Replay an ADK Agent

This is one self-contained package. It contains a **completed golden** ADK
multi-agent application plus the Class 02C observability utilities.

You do not need to complete any earlier class. You are not expected to edit or
rebuild the agent source — it is the system you will observe.

## Contents

```text
class-02C/
├── adk_multiagent_systems/       # Completed golden agent applications
├── movie_pitches/                # Generated movie-pitch files
├── scripts/                      # Package validation utilities
├── class-02C-work/               # Telemetry helpers and generated evidence
├── pyproject.toml
├── .env.api-key.example
├── .env.vertex.example
├── class_02C_instructions.md     # The Class 02C observability lab — start here
└── CLASS_02B_INSTRUCTIONS.md     # Background: how the golden app was built
```

No nested archive is required.

## Start

```bash
unzip class-02C.zip
cd class-02C
less class_02C_instructions.md
```

Create the environment and install the project:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install "google-adk[otel-gcp]==2.6.0"
```

Confirm you have the golden source before starting the lab:

```bash
python scripts/validate_starter.py
python scripts/check_progress.py
```

Every progress line must report `PASS`.

`CLASS_02B_INSTRUCTIONS.md` is included only as background reading: it explains
how the sequential, loop, and parallel topology was built. Class 02C does not
ask you to perform those build steps.
