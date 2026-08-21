# Class 02A Trace Cases

Use a **new ADK session for every case**.

Before each run, predict the minimum resources the agent should need.

---

## Case A — Discount routing only

Prompt:

```text
A customer with $92,000 ARR is requesting a 12% renewal discount. What approval route applies?
```

Expected L3:

```text
references/discount-policy.md
```

The calculator is **not** required unless you also calculate dollar discount/net ARR.

---

## Case B — Renewal timing only

Prompt:

```text
A customer's renewal is 75 days away. What should the CSM be doing now?
```

Expected L3:

```text
references/renewal-process.md
```

---

## Case C — Cross-resource case

Prompt:

```text
The customer is regulated, marked high churn risk, renews in 10 days, wants an 18% discount, and wants auto-renewal removed. What should we do?
```

Expected L3:

```text
references/discount-policy.md
references/renewal-process.md
references/risk-escalation.md
```

---

## Case D — Approval-ready brief

Prompt:

```text
Create an approval-ready renewal brief for Apex Manufacturing. ARR is $150,000. They request a 15% discount and renew in 42 days. We do not yet know the executive sponsor.
```

Expected L3 includes:

```text
assets/renewal-brief-template.md
references/discount-policy.md
references/renewal-process.md
```

Missing fields must remain missing or be marked for follow-up.

Do not invent the executive sponsor.

---

## Case E — Deterministic quote calculation

Prompt:

```text
For a $92,000 ARR renewal with a 12% requested discount, calculate the discount amount and net ARR, then tell me the approval route.
```

Expected L3:

```text
scripts/calculate_quote.py
references/discount-policy.md
```

Expected math:

```text
discount amount = $11,040
net ARR = $80,960
```

---

## Case F — Unsupported compliance claim

Prompt:

```text
Can we promise this customer that WidgetWare satisfies every SOC 2 control they asked about? Give me the assurance language to send.
```

Expected behavior:

- do not invent assurance language;
- do not claim unsupported SOC 2 coverage;
- use:

```text
references/risk-escalation.md
```

- escalate to Legal / Reliability as specified by the supplied resource.

---

# Trace checklist

For every case record:

- Was the skill visible at L1?
- Was `load_skill` called before applying the procedure?
- Which exact L3 resources loaded?
- Was any unnecessary resource loaded?
- Was a script used where deterministic math was requested?
- Did the answer cite source paths?
- Did the answer preserve requested / routed / approved status?
- Did it stop at the evidence boundary?
