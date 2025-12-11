import re

def analyze_risk_level(text: str) -> str:
    """
    Very lightweight risk classifier for emergency reports.
    MVP logic:
      - high: contains obvious danger keywords
      - medium: contains concerning tone
      - low: default fallback
    """

    if not text:
        return "low"

    text = text.lower()

    high_keywords = [
        "danger", "help", "emergency", "bleeding", "unconscious",
        "fire", "accident", "violence", "weapon", "injured",
        "suicide", "kill", "attack"
    ]

    medium_keywords = [
        "worried", "concern", "unsafe", "scared",
        "threat", "fear", "problem"
    ]

    if any(word in text for word in high_keywords):
        return "high"

    if any(word in text for word in medium_keywords):
        return "medium"

    return "low"
