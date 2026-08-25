---
name: code-review
description: >-
  Use this skill when the user wants to review code for issues, best practices,
  and potential improvements. Activates the code review workflow that analyzes
  code quality, identifies problems by severity, and provides actionable
  recommendations.
---

# Code Review Skill

This skill enables the agent to perform structured code reviews on user-provided
code snippets or files.

## Workflow

1. **Receive Code**: Accept the code from the user and acknowledge what was
   received (language, size, structure).
2. **Analyze**: Use the `review_code` tool to perform the review by executing [review_code.py](./scripts/review_code.py). The tool
   categorizes findings by severity:
   - **Critical**: Bugs, security vulnerabilities, logic errors
   - **Warning**: Missing documentation, potential maintainability issues
   - **Suggestion**: Style improvements, best practice recommendations
3. **Summarize**: Use the `summarize_review` tool to create a prioritized
   action list from the raw findings using [summarize_review.py](./scripts/summarize_review.py).
4. **Present**: Return a clear, structured summary to the user with:
   - A severity breakdown (critical / warning / suggestion counts)
   - Prioritized action items
   - An overall assessment

## Example Prompts

- "Review this code: `def add(a, b): return a + b`"
- "Check this function for issues and best practices"
- "What improvements can I make to this code?"

## Resources

- [review_response.txt](./resources/review_response.txt): The template file used for standard code review responses.
- [summary_response.txt](./resources/summary_response.txt): The template file used for standard code review summaries.

## Notes

- Tools are currently **placeholders** returning demo data.
- Future implementation will integrate static analysis and LLM-powered review.
