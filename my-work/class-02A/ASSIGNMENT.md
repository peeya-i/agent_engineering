# Class 02A Assignment — Engineer the Renewal Advisor Skill

## Mission

Build a reliable **WidgetWare Renewal Desk** skill using progressive disclosure.

The supplied L3 resources contain the business rules. Your work is to engineer how the agent:

1. discovers the skill at L1;
2. loads the full procedure at L2;
3. loads only the required L3 resources;
4. uses deterministic execution when required;
5. cites its evidence;
6. refuses or escalates when the evidence boundary is reached.

---

# Task 1 — Establish the baseline

Before changing `SKILL.md`:

```bash
python -m pytest -q tests/test_starter_integrity.py
python -m pytest -q
```

The starter integrity test should pass.

The full assignment suite should fail because the skill is incomplete.

Run the first two prompts in `CASES.md` and inspect the trace.

Record baseline observations in `submission.md`.

---

# Task 2 — Engineer L1 metadata

Edit the YAML frontmatter description in:

```text
renewal_desk_agent/skills/renewal-advisor/SKILL.md
```

L1 must make the skill discoverable for:

- renewal discount routing;
- renewal timing / auto-renewal questions;
- churn, legal, security, and regulated-customer risk;
- renewal quote calculations;
- approval-ready renewal briefs.

It must also exclude unrelated product troubleshooting.

Do **not** put approval thresholds or detailed policy rules in L1.

---

# Task 3 — Engineer L2 instructions

The body of `SKILL.md` is the L2 procedure.

It must tell the agent:

- when to use the skill;
- when not to use the skill;
- required inputs;
- what to do when an input is missing;
- how to classify the user's request;
- the exact L3 path for each intent;
- the minimum-resource-loading rule;
- how and where to cite evidence;
- when to use the deterministic quote script;
- how to preserve requested vs routed vs approved status;
- what to do for unsupported questions;
- what to do when a named resource cannot be loaded.

---

# Task 4 — Use exact L3 routing

Your L2 instructions must name these exact paths:

| Intent | L3 path |
|---|---|
| Discount approval/routing | `references/discount-policy.md` |
| Renewal timing / auto-renewal | `references/renewal-process.md` |
| Churn / security / legal / regulated risk | `references/risk-escalation.md` |
| Approval-ready brief | `assets/renewal-brief-template.md` |
| Dollar discount / net ARR math | `scripts/calculate_quote.py` |

Do not tell the agent to "look in the references folder."

Give it exact paths.

---

# Task 5 — Run cases A–F

Use `CASES.md`.

For each case:

1. Predict the minimum L3 resource set.
2. Start a new ADK session.
3. Run the prompt.
4. Inspect L1, L2, and L3 tool calls.
5. Compare actual vs predicted loading.
6. Check the final answer for grounding and state language.
7. Record the result in `submission.md`.

---

# Task 6 — Test safe abstention

Case F asks for a SOC 2 assurance not supported by the supplied resources.

A correct system must:

- not invent a compliance claim;
- say the supplied sources do not establish the requested claim;
- use the risk/escalation resource;
- route the issue to the appropriate human function.

Grounded refusal is success.

---

# Task 7 — Run tests and grader

```bash
python -m pytest -q
python grader.py
```

Your implementation is complete only when both pass.

---

# Task 8 — Review and submit

```bash
git status
git diff
```

Check for:

- secrets;
- accidental `.env` commits;
- policy copied into L1;
- guessed filenames;
- "approved" language without actual approval;
- unsupported claims;
- changes to supplied policies made only to satisfy the model.

Then commit and push your Class 02A work.
