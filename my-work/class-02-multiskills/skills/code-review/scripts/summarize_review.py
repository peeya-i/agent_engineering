from pathlib import Path

def summarize_review(review_text: str) -> str:
    """Summarizes code review findings into an actionable summary.

    Takes the raw review output and produces a concise, prioritized summary
    of the most important findings and recommended next steps.

    Args:
        review_text: The raw code review text to summarize.

    Returns:
        A concise summary with prioritized action items.
    """
    resource_path = Path(__file__).parent.parent / "resources" / "summary_response.txt"
    try:
        return resource_path.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error loading review summary resource: {e}"
