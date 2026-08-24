# Class 02A Submission

## Student
- Name: Peeya Iwagoshi
- GitHub: peeya-i
- Branch / commit: https://github.com/peeya-i/agent_engineering/tree/main/agent-engineering-book/Gemini/1-Foundations/Classes/class-02A 
a0abbf9e6448138ff3ac941c1a006a9cb7b5bbdc

---

# Baseline observations

## L1
For Case A: SKILL.md \
For Case B: SKILL.md


## L2
For Case A: renewal-advisor \
For Case B: renewal-advisor


## L3
For Case A: Resource 'references/policy.md' not found in skill 'renewal-advisor'. \
For Case B: reference/timeline.md, reference/policy.md,


---

# Final trace evidence

## Case A
- Predicted L3: references/discount-policy.md
- Observed L1: renewal-advisor
- Observed L2: renewal-advisor
- Observed L3: references/discount-policy.md
- Final result: Based on the WidgetWare renewal discount policy (references/discount-policy.md), a requested discount of 12% falls into the >10%–15% discount band for a customer with $92,000 ARR.
    - Current State: Requested (12% discount requested)
    - Approval Route: Routed to Customer Success Director
- Unnecessary resources loaded: None
## Case B
- Predicted L3: references/renewal-process.md
- Observed L1: renewal-advisor
- Observed L2: renewal-advisor
- Observed L3: references/renewal-process.md
- Final result: According to WidgetWare's renewal process (references/renewal-process.md), when a customer's renewal is 60–89 days away (in this case, 75 days away), the Customer Success Manager (CSM) should be focusing on:
    1. Validating the commercial path
    2. Confirming the decision process
    3. Reviewing auto-renewal notice requirements (if applicable)
- Unnecessary resources loaded: None
## Case C
- Predicted L3: references/discount-policy.md, references/renewal-process.md, references/risk-escalation.md
- Observed L1: renewal-advisor
- Observed L2: renewal-advisor
- Observed L3: references/discount-policy.md, references/renewal-process.md, references/risk-escalation.md
- Final result: Based on WidgetWare renewal policies and guidance (references/discount-policy.md, references/renewal-process.md, references/risk-escalation.md), here is what we must do:
    1. Identify Missing Information
        - Current ARR: The customer's current Annual Recurring Revenue (ARR) is missing. We need the ARR value to calculate the exact dollar discount and net ARR (via scripts/calculate_quote.py).
    2. Discount Approval Routing
        - Status: The customer requested an 18% discount.
        - Routing: According to the discount policy (references/discount-policy.md), a requested discount >15%–20% must be routed to VP, Customer Success.
        - Note: This discount is currently requested and routed to VP, Customer Success for review. It is NOT approved.
    3. Renewal Timing & Auto-Renewal Removal
        - Renewal Timing: With only 10 days remaining until renewal (references/renewal-process.md), unresolved commercial and legal blockers are treated as urgent.
        - Auto-Renewal Request: The customer requested to remove auto-renewal. Per policy, we must not promise removal based solely on a customer request; since we are inside 30 days to renewal, this must be treated as urgent and routed to Legal for contract review.
    4. Risk Escalation (Regulated & High Churn Risk)
        - Status: The customer is regulated and marked high churn risk, with multiple urgent factors within the 30-day window (references/risk-escalation.md).
        - Required Escalations:
            - Commercial / Churn Risk: Escalate to Customer Success leadership.
            - Contract Terms / Auto-Renewal Exception: Escalate to Legal.
            - Regulated Compliance / Assurance: If the customer requests compliance commitments or security assurances, do not invent claims or guarantees; escalate to Reliability/Security and Legal.
    - Recommended Next Steps for CSMs:
        1. Provide the current ARR so the exact quote calculations can be performed.
        2. Route the 18% discount request to the VP, Customer Success.
        3. Escalate the auto-renewal removal request and regulated contract terms to Legal immediately (given the 10-day window).
        4. Notify Customer Success leadership regarding the high churn risk status within the 30-day urgent renewal window.
- Unnecessary resources loaded: scripts/calculate_quote.py
## Case D
- Predicted L3: assets/renewal-brief-template.md, references/discount-policy.md, references/renewal-process.md
- Observed L1: renewal-advisor
- Observed L2: renewal-advisor
- Observed L3: assets/renewal-brief-template.md, references/discount-policy.md, references/renewal-process.md
- Final result:
### WidgetWare Renewal Approval Brief
#### Account
- **Customer**: Apex Manufacturing
- **ARR**: $150,000.00
- **Renewal date / days remaining**: 42 days remaining (falling within the 30–59 days milestone window)
- **Customer segment**: Commercial
- **Executive sponsor**: Unknown (Pending follow-up)
#### Request
- **Requested commercial change**: Renewal with a 15% discount
- **Requested discount**: 15%
- **Auto-renewal / contract request**: None specified
#### Evidence
- **Relevant customer facts**: ARR is $150,000; customer requests a 15% discount; 42 days remaining until renewal.
- **Missing facts**: Executive sponsor is not yet known.
#### Policy routing
- **Discount approval route**: Routed to Customer Success Director (>10%–15% discount policy band per references/discount-policy.md)
- **Timing/process actions**: Finalize commercial options, approval dependencies, and customer action plan (30–59 days window per references/renewal-process.md)
- **Risk/legal/security escalations**: None triggered currently, pending executive sponsor identification and stakeholder engagement
#### Financial calculation
- **List ARR**: $150,000.00
- **Discount amount**: $22,500.00
- **Net ARR**: $127,500.00
#### Status
- **Requested**: 15% discount requested by customer
- **Routed**: Routed to Customer Success Director (pending review/approval)
- **Approved**: Pending (not yet approved)
#### Human decisions required
- **Identify and confirm the executive sponsor for Apex Manufacturing**.
- **Customer Success Director review and approval decision on the requested 15% discount**.


- **Unnecessary resources loaded**: None

## Case E
- Predicted L3: scripts/calculate_quote.py, references/discount-policy.md
- Observed L1: renewal-advisor
- Observed L2: renewal-advisor
- Observed L3: scripts/calculate_quote.py, references/discount-policy.md
- Final result:
    - For a renewal with a list ARR of $92,000 and a requested discount of 12%:
        - **Discount Amount**: $11,040.00
        - **Net ARR**: $80,960.00
    - **Approval Route**:
        - According to WidgetWare's renewal discount policy (references/discount-policy.md), requested discounts greater than 10% up to 15% fall into the routing band for the Customer Success Director.
        - **Status**: Requested (routed to Customer Success Director).

- **Unnecessary resources loaded**: None

## Case F
- Predicted L3: references/risk-escalation.md
- Observed L1: renewal-advisor
- Observed L2: renewal-advisor
- Observed L3: references/risk-escalation.md
- Final result:
    - No, we cannot promise that WidgetWare satisfies every SOC 2 control the customer asked about. 
    - Based on WidgetWare renewal and risk escalation policy (`references/risk-escalation.md`), we must never invent SOC 2 control coverage, security certifications, or compliance commitments. When a regulated customer asks about compliance or security assurance that is not verified by established policy or evidence, we cannot provide assurance language.
    - **Status and Next Steps**
        - **Requested State:** Customer requested SOC 2 control assurance for all asked items.
        - **Routed State:** Routed to Reliability/Security and Legal for review.
    - **Please do not send any compliance assurance language at this time.** This request has been escalated to Reliability/Security and Legal to verify our actual SOC 2 control coverage before responding to the customer.
- Unnecessary resources loaded: None

---

# What I learned

## Skill vs resource
Skill files (L1/L2) define discovery metadata and operating procedures, whereas L3 resources provide granular domain policy, assets, and scripts loaded only on demand.
## L1 → L2 → L3 progressive disclosure
Progressive disclosure minimizes context window overhead by exposing skill triggers at L1, operating instructions at L2, and specific reference documents at L3 only when required by user intent.
## Why minimum-resource loading matters
Loading only the minimum necessary resources avoids context pollution, prevents hallucinations from unneeded rules, reduces token latency, and lowers overall API costs.
## Why deterministic math belongs in a script
Executing code scripts guarantees exact, reproducible arithmetic for dollar amounts and net ARR, avoiding LLM math errors and precision drift.
## Why safe abstention can be a correct answer
When evidence or authorization is missing, safe abstention prevents the agent from making up unbacked compliance or legal guarantees, ensuring proper human escalation.
