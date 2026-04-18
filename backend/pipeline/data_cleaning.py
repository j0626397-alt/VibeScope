import re
import html


def clean_html_tags(text: str) -> str:
    """Remove HTML tags from text."""
    clean = re.compile(r"<[^>]+>")
    return clean.sub("", text)


def remove_urls(text: str) -> str:
    """Remove URLs from text."""
    url_pattern = re.compile(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|"
        r"(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    )
    return url_pattern.sub("", text)


def remove_emojis(text: str) -> str:
    """Remove emoji characters."""
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub("", text)


def remove_special_chars(text: str) -> str:
    """Remove special characters, keep alphanumeric and basic punctuation."""
    return re.sub(r"[^\w\s.,!?'-]", " ", text)


def normalize_whitespace(text: str) -> str:
    """Normalize whitespace."""
    return " ".join(text.split())


def truncate_tokens(text: str, max_tokens: int = 512) -> str:
    """Truncate text to approximate token count (rough estimate: 1 token ≈ 4 chars)."""
    max_chars = max_tokens * 4
    return text[:max_chars]


def clean_text(text: str) -> str:
    """Full cleaning pipeline."""
    if not text or not isinstance(text, str):
        return ""

    text = html.unescape(text)
    text = clean_html_tags(text)
    text = remove_urls(text)
    text = remove_emojis(text)
    text = remove_special_chars(text)
    text = normalize_whitespace(text)
    text = text.strip()
    text = truncate_tokens(text)

    return text


def is_valid_text(text: str, min_length: int = 5) -> bool:
    """Check if text is valid for analysis."""
    return bool(text and len(text.strip()) >= min_length)
