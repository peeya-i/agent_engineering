# Agent Engineering Lab: Progressive Skills and Resources

## Mission

Build a policy-grounded **WidgetWare Renewal Desk Agent**. The agent must help a customer-success manager evaluate renewal requests without placing every policy, template, and calculation rule in the agent's permanent prompt.

You will use progressive disclosure:

| Level | What the agent receives | ADK interaction | Purpose |
| --- | --- | --- | --- |
| L1 — Metadata | Skill name and description | `list_skills` / injected catalog | Decide whether the skill is relevant |
| L2 — Instructions | Full body of `SKILL.md` | `load_skill` | Learn the procedure and resource-routing rules |
| L3 — Resources | Selected references, assets, or scripts | `load_skill_resource` / `run_skill_script` | Load only the evidence or executable needed now |

The important design constraint is **selective loading**. A good agent does not load every L3 file for every request.

## Learning objectives

By the end of the lab, you should be able to:

1. Distinguish a prompt, skill, tool, workflow, and resource.
2. Design L1 metadata that routes accurately without leaking the entire policy.
3. Write L2 instructions containing triggers, procedure, quality rules, and exact resource paths.
4. Use L3 references, an asset, and a deterministic script only when needed.
5. Verify resource use in the ADK trace.
6. Refuse or escalate when the supplied resources do not support an answer.

## Scenario

WidgetWare renews enterprise software contracts. Customer-success managers need help with:

- Discount approval routing
- Renewal timing and commercial process
- Risk escalation
- Renewal briefs for approvers
- Deterministic quote calculations

The source documents are already provided. Your job is to engineer the skill, not invent policy.

## Timebox

90 minutes:

- 10 min — Setup and baseline
- 15 min — L1 metadata
- 25 min — L2 instructions
- 25 min — L3 resources and trace exercises
- 10 min — Evaluation and fixes
- 5 min — Reflection

## Rules

- Edit `renewal_desk_agent/skills/renewal-advisor/SKILL.md`.
- Do not paste policy facts into `agent.py`.
- Do not copy the full reference documents into `SKILL.md`.
- Cite every policy conclusion using the exact relative path, for example `[Source: references/discount-policy.md]`.
- Load only the minimum L3 resources needed for a request.
- Never invent an approval, deadline, control ID, or policy exception.
- If a resource or script path fails, do not guess several filenames. Report the missing path and stop.

## Assignment

### Task 1 — Establish the baseline

1. Complete the setup in `SETUP.md`.
2. Start ADK Web.
3. Ask: `What specialist skills are available to you? Give only their names and descriptions.`
4. Inspect the trace and record what was visible at L1 in `SUBMISSION.md`.
5. Ask: `A customer asked for a renewal discount. What should I do?`
6. Record the weaknesses of the starter skill before editing it.

### Task 2 — Engineer L1 metadata

Replace the placeholder description in `SKILL.md` with a description that:

- States the capability and the main trigger situations.
- Is specific enough to select for renewal, discount, escalation, and renewal-brief questions.
- Does not contain approval thresholds or other policy facts.
- Does not trigger for unrelated product troubleshooting.

Run `pytest -q` after making the change.

### Task 3 — Engineer L2 instructions

Complete the body of `SKILL.md`. It must include:

1. When to use and when not to use the skill.
2. Required inputs and how to handle missing inputs.
3. A step-by-step procedure.
4. An exact routing map from question type to L3 file path.
5. A minimum-resource rule.
6. Citation and output requirements.
7. Refusal/escalation behavior for unsupported questions.
8. Positive, negative, and ambiguous examples.

The L2 file should tell the agent **how to work** and **where to look**. The L3 files remain the source of detailed truth.

### Task 4 — Demonstrate selective L3 loading

Run the following prompts one at a time in new sessions. For each, inspect the trace and record the loaded files in `SUBMISSION.md`.

#### Case A — One reference

`The renewal ARR is $92,000 and the requested discount is 12%. Which approval path is required?`

Expected behavior: load the discount policy only, state the approval path, and cite it.

#### Case B — A different single reference

`The renewal date is 75 days away. What should the CSM do now?`

Expected behavior: load the renewal process only.

#### Case C — Cross-resource reasoning

`Northstar is a regulated customer, churn risk is high, renewal is in 10 days, and it requests an 18% discount plus removal of auto-renewal. Prepare the action plan.`

Expected behavior: load all and only the policy references needed to combine commercial, timing, and risk guidance.

#### Case D — Asset use

`Create an approval-ready renewal brief for Northstar using the official format. ARR is $150,000, discount is 18%, renewal is in 10 days, risk is high, and the customer asks to remove auto-renewal.`

Expected behavior: load the official template plus the policy references required to complete it. Do not fabricate missing fields.

#### Case E — Script use

`Calculate the net ARR and dollar discount for $92,000 ARR at 12%. Use the deterministic calculator, then state the approval path.`

Expected behavior: run the exact calculator script for arithmetic and load the discount policy for approval.

#### Case F — Unsupported question

`Give me the exact SOC 2 control ID that allows us to promise a 24-hour recovery time.`

Expected behavior: state that the provided sources do not support the requested control ID or promise, then name the proper escalation route. Do not invent an answer.

### Task 5 — Evaluate and improve

1. Run `pytest -q` until all structural tests pass.
2. Run every case in `eval/eval-cases.json` manually through ADK Web.
3. Give each case a score of 0 or 1 for each criterion:
   - Correct skill selection
   - Minimum resource loading
   - Factual correctness
   - Required citation
   - Safe unsupported handling
4. Fix `SKILL.md` if any case scores below 4/5.

### Task 6 — Submit

Submit:

- Completed `SKILL.md`
- Completed `SUBMISSION.md`
- Screenshot or exported trace evidence for Cases A, C, E, and F
- Output of `pytest -q`
- One Git commit with the message: `complete progressive skills lab`

## Definition of done

Your agent demonstrates the sequence:

`L1 discovery → L2 procedure → minimum necessary L3 evidence or execution → grounded answer`

It must also demonstrate that **not loading** an irrelevant resource is an intentional engineering behavior.

## Concept check

| Artifact | Role |
| --- | --- |
| Prompt | Instruction for this agent or interaction |
| Skill | Reusable, versionable procedure or expertise |
| Resource | Detail loaded by a skill only when needed |
| Tool | Capability that reads, calculates, calls, or changes something |
| Workflow | Coordinates stages, agents, state, and control flow |

Official reference: [ADK Skills documentation](https://adk.dev/skills/).
