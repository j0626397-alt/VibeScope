import re
from typing import List


def preprocess_for_sentiment(text: str) -> str:
    """Prepare text for sentiment model."""
    # Lowercase
    text = text.lower()
    # Replace user mentions with @user token
    text = re.sub(r"@\w+", "@user", text)
    # Replace hashtags
    text = re.sub(r"#(\w+)", r"\1", text)
    return text.strip()


def batch_texts(texts: List[str], batch_size: int = 16) -> List[List[str]]:
    """Split list of texts into batches."""
    return [texts[i : i + batch_size] for i in range(0, len(texts), batch_size)]


def deduplicate_texts(texts: List[str], threshold: float = 0.9) -> List[str]:
    """Remove near-duplicate texts (simple exact dedup)."""
    seen = set()
    unique = []
    for text in texts:
        normalized = " ".join(text.lower().split())
        if normalized not in seen:
            seen.add(normalized)
            unique.append(text)
    return unique


def filter_min_length(texts: List[str], min_len: int = 5) -> List[str]:
    return [t for t in texts if t and len(t.strip()) >= min_len]
