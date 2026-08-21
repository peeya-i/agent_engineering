# Class 02A Setup

This version of the lab supports **two authentication paths**. Pick one.

Do not configure both at the same time.

---

# Prerequisites

- Python 3.11+
- Git
- Google ADK
- An IDE/terminal
- For the live agent: either
  - a Gemini API key from Google AI Studio, **or**
  - Google Cloud Application Default Credentials for Vertex AI

The coding assistant inside your IDE and the model used by your ADK agent are separate authentication concerns.

---

# 1. Create the virtual environment

From the Class 02A root:

## macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

Your prompt should show something like:

```text
(.venv)
```

---

# 2. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Verify:

```bash
python -c "import google.adk; print('google-adk import: OK')"
adk --help
```

---

# 3. Create the agent `.env`

The `.env` file belongs here:

```text
renewal_desk_agent/.env
```

Copy the supplied example:

## macOS / Linux

```bash
cp renewal_desk_agent/.env.example renewal_desk_agent/.env
```

## Windows PowerShell

```powershell
Copy-Item renewal_desk_agent\.env.example renewal_desk_agent\.env
```

Never commit `.env`.

---

# 4. Choose ONE authentication mode

## Option A — Gemini API key / AI Studio

This is the simplest local-development path.

Edit:

```text
renewal_desk_agent/.env
```

Use:

```dotenv
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GEMINI_API_KEY=PASTE_YOUR_KEY_HERE
GEMINI_MODEL=gemini-3.7-flash
```

Leave the Vertex project/location values blank.

You do **not** need a Google Cloud project merely to use the Gemini API-key path.

---

## Option B — Vertex AI / Google Cloud

Use Application Default Credentials:

```bash
gcloud auth application-default login
```

Set your project:

```bash
gcloud config set project YOUR_PROJECT_ID
```

Edit:

```text
renewal_desk_agent/.env
```

Use:

```dotenv
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
GOOGLE_CLOUD_LOCATION=us-central1
GEMINI_MODEL=gemini-3.7-flash
```

Do not put a Gemini API key in the file when using this path.

Your project must have appropriate model access and billing.

---

# 5. Run the starter integrity test

```bash
python -m pytest -q tests/test_starter_integrity.py
```

This must pass before continuing.

---

# 6. Run preflight

Offline:

```bash
python scripts/preflight.py
```

Optional live check:

```bash
python scripts/preflight.py --online
```

The online check makes one tiny model request. If it fails with authentication, billing, quota, organization-policy, or model-access errors, resolve that **before** starting the trace exercise.

---

# 7. Start ADK Web

Stay in the Class 02A root:

```bash
pwd
```

You should be in the folder containing:

```text
renewal_desk_agent/
tests/
README.md
```

Then:

```bash
adk web .
```

Open the URL printed by ADK, normally:

```text
http://127.0.0.1:8000
```

or the URL shown in your terminal.

Select:

```text
renewal_desk_agent
```

---

# 8. Baseline behavior

Start a **new session**.

Ask:

```text
What skills can you use for renewal work?
```

Then:

```text
A customer with $92,000 ARR is asking for a 12% renewal discount. What should we do?
```

Inspect the trace.

The starter's L1/L2 skill content is intentionally weak. Record what is missing before fixing it.

---

# If setup fails

Read `TROUBLESHOOTING.md` before changing application code.
