def check_safety(message_content: str) -> bool:
    """Validates input to prevent prompt injection and policy violations."""
    forbidden_terms = ["ignore previous instructions", "jailbreak", "bypass"]
    for term in forbidden_terms:
        if term in message_content.lower():
            return False
    return True