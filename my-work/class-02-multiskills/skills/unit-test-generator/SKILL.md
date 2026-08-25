---
name: unit-test-generator
description: >-
  Use this skill when the user wants to generate unit tests for functions and
  methods in their codebase. Activates the test generation workflow that
  identifies testable code, produces test stubs covering happy paths, edge
  cases, and error conditions, and summarizes coverage.
---

# Unit Test Generator Skill

This skill enables the agent to generate unit test stubs for user-provided
code, covering key testing patterns.

## Workflow

1. **Receive Code**: Accept the code from the user. Identify the functions,
   methods, and classes that need tests.
2. **Generate Tests**: Use the `generate_unit_tests` tool to create test stubs by executing [generate_unit_tests.py](./scripts/generate_unit_tests.py). The tool generates tests covering:
   - **Happy path**: Normal expected behavior
   - **Edge cases**: Empty inputs, boundary values, None handling
   - **Error handling**: Exception raising and error conditions
3. **Summarize**: Use the `summarize_tests` tool to create a coverage summary with recommendations for additional tests using [summarize_tests.py](./scripts/summarize_tests.py).
4. **Present**: Return the generated test code and summary to the user with:
   - The complete test file content
   - A coverage estimate
   - Recommendations for additional test cases

## Example Prompts

- "Generate unit tests for: `def multiply(x, y): return x * y`"
- "Create test stubs for the functions in this code"
- "Write tests for this class"

## Resources

- [test_stubs.py](./resources/test_stubs.py): Python template code used for generated test stubs.
- [test_summary.txt](./resources/test_summary.txt): Template file used for the generated test summaries.

## Notes

- Tools are currently **placeholders** returning demo test stubs.
- Future implementation will use AST parsing and LLM-powered test generation.
