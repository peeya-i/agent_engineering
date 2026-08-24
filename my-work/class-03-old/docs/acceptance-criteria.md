# Acceptance Criteria

Written before any implementation exists, per Book 1 §1.7. Each criterion below is stated so that a person could test it mechanically, without asking a clarifying question.

1. **Schema conformance.** Every qualification result produced by the system validates against a published schema (introduced in Class 5 / Book 1 Chapter 6). A result that does not validate is never surfaced as if it were a valid answer.
2. **Evidence or labeled inference.** Every material factual claim in a qualification result or outreach draft either references a specific piece of supplied or retrieved evidence, or is explicitly labeled as an inference. A claim with neither is a defect.
3. **No drafting on insufficient evidence.** When the evidence available for a company does not support a qualification decision either way, the system produces `NEEDS_RESEARCH` and does not draft outreach. A drafted message for an insufficiently evidenced account is a defect.
4. **No autonomous send.** No test run, demonstration, or production path in this codebase ever transmits an outbound message without a preceding, explicit human approval. This is verified by inspecting the codebase for the absence of any send-capable tool, not merely by observing that no test happened to trigger one.
5. **Explainability.** For any qualification result, a person can ask "why this decision?" and receive an answer naming the specific matched or failed ICP criteria and the evidence behind them — not a restatement of the result itself.
6. **Usable on representative accounts.** Given the representative test accounts in `tests/scenarios/`, the system produces a result a real SDR would find usable — correct in direction, honest about uncertainty, and free of fabricated detail.

## How this differs from "the response looks good"

Each criterion above names a specific, checkable signal. None of them can be satisfied by a fluent-sounding paragraph alone.
