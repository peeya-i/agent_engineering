# Class 02A — Skills & Resources: WidgetWare Renewal Desk

## What this class teaches

This lab teaches **progressive disclosure** through a real ADK skill:

- **L1 — Metadata:** enough information to discover the right skill.
- **L2 — Instructions:** the reusable procedure in `SKILL.md`.
- **L3 — Resources:** detailed references, assets, and deterministic scripts loaded only when needed.

The starter is intentionally incomplete at **L1 and L2**. The setup itself is complete.

> Your job is to engineer the skill, not to repair the lab environment.

---

## What you edit

You should primarily edit:

```text
renewal_desk_agent/skills/renewal-advisor/SKILL.md
submission.md
```

You may make small changes elsewhere if needed, but do **not** rewrite the supplied policy resources just to make your answer easier.

The L3 files are the source-controlled evidence for the exercise.

---

## 1. Synchronize your fork from the CLI

One-time setup, if `upstream` is not already configured:

```bash
git remote add upstream https://github.com/sensei-ji/agent_engineering.git
git remote -v
```

Before starting the class:

```bash
git checkout main
git fetch upstream
git merge --ff-only upstream/main
git push origin main
```

Then copy the complete Class 02A folder into your own work area as instructed by the instructor.

Do **not** copy a Class 02 golden solution into 02A. Class 02A is self-contained.

---

## 2. Read these files in order

1. `README.md`
2. `SETUP.md`
3. `ASSIGNMENT.md`
4. `CASES.md`
5. `renewal_desk_agent/skills/renewal-advisor/SKILL.md`

Use Markdown Preview in your IDE if that makes the files easier to read.

---

## 3. Verify the starter before doing the assignment

Create and activate a virtual environment, install dependencies, then run:

```bash
python -m pytest -q tests/test_starter_integrity.py
```

Expected result:

```text
PASS
```

This proves the supplied resources, calculator, model configuration, and starter structure are healthy.

Now run:

```bash
python -m pytest -q
```

**Before you complete the skill, assignment tests are expected to fail.**

Those failures describe the learning gap: incomplete L1 metadata, incomplete L2 instructions, and an unfinished submission record.

---

## 4. Run the preflight

Offline configuration check:

```bash
python scripts/preflight.py
```

Optional live model/auth check:

```bash
python scripts/preflight.py --online
```

Run the online preflight **before** the main lab. It is designed to catch:

- missing API credentials;
- Vertex AI authentication problems;
- invalid model names;
- quota or billing failures;
- network failures.

---

## 5. Start ADK Web from the correct directory

Run this command from the **Class 02A root**, the directory that contains `renewal_desk_agent/`:

```bash
adk web .
```

Correct:

```text
class-02A/
├── renewal_desk_agent/
└── tests/

$ adk web .
```

Do **not** `cd renewal_desk_agent` and then run `adk web .`.

ADK Web discovers agent application directories beneath the directory you give it.

---

## 6. The build loop

Use this loop throughout the assignment:

```text
READ → PREDICT → RUN → TRACE → FIX → TEST → RECORD
```

For every case:

1. Predict which skill/resource should load.
2. Run the case in a **new ADK session**.
3. Inspect the trace.
4. Record exact L1 → L2 → L3 behavior.
5. Fix the skill if behavior is wrong.
6. Re-run tests.
7. Record the final result in `submission.md`.

---

## 7. Final verification

```bash
python -m pytest -q
python grader.py
```

Both must pass.

Then review:

```bash
git status
git diff
```

Commit and push your work.

---

## Important boundaries

- A **skill** is reusable instruction/procedure, not model training.
- A **resource** is detailed knowledge, template, or executable content loaded only when required.
- A **tool** executes an action.
- A **workflow** controls sequencing/state.
- Requested, routed, and approved are different commercial states.
- Never invent a policy rule or compliance claim.
- A grounded refusal is a correct result when the supplied resources do not support the requested claim.
