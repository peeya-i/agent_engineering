---
name: renewal-advisor
description: "Use for WidgetWare commercial renewals, including renewal discount routing, renewal timing and auto-renewal milestones, churn/legal/security/regulated risk escalation, deterministic renewal quote calculations, and creating approval-ready renewal briefs. Do NOT use for general product troubleshooting or technical support."
---

# Renewal Advisor Operating Procedure

## Purpose and Scope
Use this skill for handling WidgetWare commercial renewals, including routing discount approvals, tracking renewal timing milestones, handling risk escalations, performing quote calculations, and assembling renewal briefs.

### When to Use
Use when a prompt involves:
- Renewal discount approval routing and policy checks.
- Renewal timing, process milestones, or auto-renewal contract terms.
- High churn risk, legal, security, or regulated customer risk escalations.
- Calculating exact dollar discount and net ARR values for a renewal quote.
- Assembling approval-ready renewal briefs for leadership review.

### When Not to Use
Do NOT use this skill for:
- General product troubleshooting or technical support inquiries.
- Non-renewal sales or general product documentation.

---

## Required Inputs & Handling Missing Inputs
Identify all required inputs based on intent:
- **Discount routing**: ARR and requested discount percentage.
- **Timing & milestones**: Days remaining until renewal date.
- **Risk escalation**: Churn risk status, regulatory requirements, legal terms, or security concerns.
- **Renewal brief**: Account name, ARR, renewal date, requested terms, executive sponsor.

If an input is missing or ambiguous:
- For quote math or discount routing: ask the user for the missing ARR or discount percentage before calculating or routing.
- For renewal briefs: keep missing fields explicitly marked as missing or pending follow-up (do not invent missing data such as executive sponsors).

---

## Intent Classification & Exact L3 Resource Routing

### Minimum Resource Loading Rule
Load ONLY the single exact L3 resource required for the classified intent. Do not load unneeded references.

| User Intent | Required Action / L3 Path |
|---|---|
| Discount approval & routing | Load `references/discount-policy.md` |
| Renewal timing & auto-renewal process | Load `references/renewal-process.md` |
| Churn, legal, security, & regulated customer risk | Load `references/risk-escalation.md` |
| Approval-ready renewal brief | Load `assets/renewal-brief-template.md` (and related references as needed) |
| Dollar discount & net ARR calculations | Run `scripts/calculate_quote.py` |

If a named resource cannot be loaded or is missing, state clearly that the resource is unavailable and escalate to human review.

---

## Operating Contracts

### Deterministic Quote Calculations
When calculating dollar discount or net ARR, always execute `scripts/calculate_quote.py` with `--arr` and `--discount-percent`. Do not rely on LLM mental arithmetic for financial values.

### Evidence Citation & Safety Boundaries
- Always cite the exact source path (e.g. `references/discount-policy.md`) when providing policy guidance, routing, or process steps.
- **State Language Discipline**: Strictly preserve state distinctions:
  - Mark status as `requested` when describing customer requests.
  - Mark status as `routed` (or `routed to <role>`) after determining the appropriate approval authority.
  - Mark status as `approved` ONLY when explicit approval evidence is present in the context. Never treat falling into a routing band as an approval.
- **Safe Abstention & Unsupported Claims**: For unsupported questions or unverified compliance claims (e.g., SOC 2 control guarantees not established by supplied sources), do not invent claims or assurance language. State that supplied sources do not establish the claim, cite `references/risk-escalation.md`, and route to Legal or Reliability/Security.
