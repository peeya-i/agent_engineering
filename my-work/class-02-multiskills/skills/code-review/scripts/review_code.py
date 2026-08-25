from pathlib import Path

def review_code(code: str) -> str:
    """Reviews the provided code for issues, best practices, and improvements.

    Analyzes the given code snippet and returns a structured review with
    findings categorized by severity (critical, warning, suggestion).

    Args:
        code: The source code to review as a string.

    Returns:
        A structured review summary with categorized findings.
    """
    resource_path = Path(__file__).parent.parent / "resources" / "review_response.txt"
    try:
        content = resource_path.read_text(encoding="utf-8")
        return f"Code analyzed ({len(code)} characters):\n──────────────────────────\n" + content
    except Exception as e:
        return f"Error loading review resource: {e}"
