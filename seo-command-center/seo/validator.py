"""
validator.py — helper tools for the Fixer Agent to validate its rewrites.
"""

def validate_title(text: str) -> tuple[bool, str]:
    """Check if title is <= 60 chars and <= 561 pixels."""
    if not text:
        return False, "Title is empty"

    # Length check
    if len(text) > 60:
        return False, f"Too long: {len(text)} chars (max 60)"

    # Pixel approximation: avg char ~9.2px
    # In a real env, this would use a proper font-metric library
    px = len(text) * 9.2
    if px > 561:
        return False, f"Too wide: ~{int(px)}px (max 561px)"

    return True, "Valid"

def validate_meta(text: str) -> tuple[bool, str]:
    """Check if meta description is <= 155 chars."""
    if not text:
        return False, "Meta description is empty"
    if len(text) > 155:
        return False, f"Too long: {len(text)} chars (max 155)"
    return True, "Valid"
