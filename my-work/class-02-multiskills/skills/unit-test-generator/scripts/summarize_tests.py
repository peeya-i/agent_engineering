from pathlib import Path

def summarize_tests(test_code: str) -> str:
    """Summarizes the generated unit tests and their coverage.

    Takes the generated test code and produces a summary of what is covered,
    what patterns are tested, and recommendations for additional tests.

    Args:
        test_code: The generated unit test code to summarize.

    Returns:
        A summary of test coverage and recommendations.
    """
    resource_path = Path(__file__).parent.parent / "resources" / "test_summary.txt"
    try:
        return resource_path.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error loading test summary resource: {e}"
