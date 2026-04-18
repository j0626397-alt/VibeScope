"""
Sentiment analysis using cardiffnlp/twitter-roberta-base-sentiment
Exact implementation from the notebooks:
  - AutoTokenizer + AutoModelForSequenceClassification
  - scipy softmax on raw logits
  - argmax to pick label
  - labels = ["negative", "neutral", "positive"]
"""

import os
import torch
import numpy as np
from scipy.special import softmax
from functools import lru_cache
from typing import List, Dict

os.environ["TOKENIZERS_PARALLELISM"] = "false"

MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment"
LABELS = ["negative", "neutral", "positive"]


@lru_cache(maxsize=1)
def _load_model():
    """Load tokenizer and model once, cache forever."""
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    print(f"[Sentiment] Loading {MODEL_NAME} ...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    model.eval()
    print("[Sentiment] Model loaded.")
    return tokenizer, model


def analyze_sentiment(text: str) -> Dict:
    """
    Analyze a single text — mirrors notebook implementation exactly:
      encoded = tokenizer(text, return_tensors="pt", truncation=True)
      output  = model(**encoded)
      scores  = softmax(output.logits[0].detach().numpy())
      label   = labels[scores.argmax()]
    """
    if not text or len(text.strip()) < 3:
        return {"label": "neutral", "score": 0.5, "scores": {"negative": 0.1, "neutral": 0.8, "positive": 0.1}}

    try:
        tokenizer, model = _load_model()

        encoded = tokenizer(
            text[:512],
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        with torch.no_grad():
            output = model(**encoded)

        raw_scores = output.logits[0].detach().numpy()
        probs = softmax(raw_scores)          # [neg_prob, neu_prob, pos_prob]

        idx = int(np.argmax(probs))
        label = LABELS[idx]
        score = float(probs[idx])

        return {
            "label": label,
            "score": round(score, 4),
            "scores": {
                "negative": round(float(probs[0]), 4),
                "neutral":  round(float(probs[1]), 4),
                "positive": round(float(probs[2]), 4),
            }
        }

    except Exception as e:
        print(f"[Sentiment] Error: {e}")
        return {"label": "neutral", "score": 0.5, "scores": {"negative": 0.1, "neutral": 0.8, "positive": 0.1}}


def batch_analyze_sentiment(texts: List[str], batch_size: int = 8) -> List[Dict]:
    """Batch version — calls analyze_sentiment per item (model is cached)."""
    results = []
    for text in texts:
        results.append(analyze_sentiment(text))
    return results


def compute_sentiment_distribution(sentiments: List[str]) -> Dict[str, float]:
    """Compute % distribution of positive / neutral / negative."""
    if not sentiments:
        return {"positive": 0.0, "neutral": 0.0, "negative": 0.0}

    total = len(sentiments)
    counts = {"positive": 0, "neutral": 0, "negative": 0}
    for s in sentiments:
        if s in counts:
            counts[s] += 1

    return {k: round((v / total) * 100, 1) for k, v in counts.items()}
