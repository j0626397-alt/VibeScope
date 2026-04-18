"""
Keyword extraction using NLTK stopwords (from notebooks).
Also builds word cloud frequency data.
"""

import re
from collections import Counter
from typing import List, Dict
import nltk

# Download stopwords silently on first use
try:
    from nltk.corpus import stopwords
    stopwords.words("english")
except LookupError:
    nltk.download("stopwords", quiet=True)

# Custom stopwords matching notebook's custom_stopwords
CUSTOM_STOPWORDS = {
    "video", "like", "just", "dont", "know", "hai", "kya",
    "yeh", "bhai", "sir", "bro", "one", "get", "also",
    "would", "could", "said", "says", "new", "will", "also",
    "even", "really", "think", "still", "much", "many",
    "amp", "http", "https", "com", "www", "via",
}


def _get_stopwords() -> set:
    try:
        from nltk.corpus import stopwords as sw
        return set(sw.words("english")).union(CUSTOM_STOPWORDS)
    except Exception:
        # fallback minimal set
        return {
            "the","a","an","and","or","but","in","on","at","to","for","of",
            "with","by","from","is","are","was","were","be","been","have",
            "has","had","do","does","did","will","would","could","should",
            "may","might","can","that","this","these","those","it","its",
            "i","me","my","we","our","you","your","he","she","they","them",
            "their","what","which","who","how","when","where","why","all",
            "some","not","no","so","if","as","just","about","more",
        }.union(CUSTOM_STOPWORDS)


def extract_keywords_nltk(texts: List[str], top_n: int = 10) -> List[str]:
    """
    Extract top keywords using NLTK — mirrors notebook:
      text = re.sub(r"[^a-zA-Z\s]", "", text)
      words = text.split()
      filtered = [w for w in words if w not in stop_words and len(w) > 2]
      word_counts = Counter(filtered)
      top_keywords = word_counts.most_common(20)
    """
    stop_words = _get_stopwords()
    word_freq: Counter = Counter()

    for text in texts:
        if not text:
            continue
        # Exact notebook preprocessing
        t = re.sub(r"http\S+", "", text.lower())
        t = re.sub(r"[^a-zA-Z\s]", "", t)
        words = t.split()
        filtered = [w for w in words if w not in stop_words and len(w) > 2]
        word_freq.update(filtered)

    return [word for word, _ in word_freq.most_common(top_n)]


def build_wordcloud_data(texts: List[str], top_n: int = 60) -> Dict[str, int]:
    """Build word → frequency dict for the word cloud widget."""
    stop_words = _get_stopwords()
    word_freq: Counter = Counter()

    for text in texts:
        if not text:
            continue
        t = re.sub(r"http\S+", "", text.lower())
        t = re.sub(r"[^a-zA-Z\s]", "", t)
        words = t.split()
        filtered = [w for w in words if w not in stop_words and len(w) > 2]
        word_freq.update(filtered)

    return dict(word_freq.most_common(top_n))
