"""
Emotion detection using j-hartmann/emotion-english-distilroberta-base
Exact implementation from the notebooks:
  - pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
  - result[0]["label"]  ->  anger | disgust | fear | joy | neutral | sadness | surprise

We map these 7 HuggingFace labels to the 5 dashboard labels:
  joy      -> happy
  anger    -> anger
  disgust  -> anger
  fear     -> sadness
  sadness  -> sadness
  surprise -> excitement
  neutral  -> neutral
"""

import os
from functools import lru_cache
from typing import List, Dict

os.environ["TOKENIZERS_PARALLELISM"] = "false"

EMOTION_MODEL = "j-hartmann/emotion-english-distilroberta-base"

# Map HuggingFace 7-class labels -> our 5 dashboard labels
HF_TO_DISPLAY = {
    "joy":      "happy",
    "anger":    "anger",
    "disgust":  "anger",
    "fear":     "sadness",
    "sadness":  "sadness",
    "surprise": "excitement",
    "neutral":  "neutral",
}

DISPLAY_LABELS = ["happy", "anger", "sadness", "excitement", "neutral"]


@lru_cache(maxsize=1)
def _load_emotion_pipeline():
    from transformers import pipeline
    print(f"[Emotion] Loading {EMOTION_MODEL} ...")
    pipe = pipeline(
        "text-classification",
        model=EMOTION_MODEL,
        return_all_scores=False,
    )
    print("[Emotion] Model loaded.")
    return pipe


def detect_emotion(text: str) -> str:
    """
    Detect emotion for a single text.
    Mirrors notebook exactly:
      result = emotion_model(text[:512])[0]
      return result["label"]
    Then mapped to display label.
    """
    if not text or len(text.strip()) < 3:
        return "neutral"

    try:
        pipe = _load_emotion_pipeline()
        result = pipe(str(text)[:512])[0]
        hf_label = result["label"]
        return HF_TO_DISPLAY.get(hf_label, "neutral")
    except Exception as e:
        print(f"[Emotion] Error: {e}")
        return "neutral"


def batch_detect_emotions(texts: List[str]) -> List[str]:
    """Detect emotions for a list of texts."""
    return [detect_emotion(t) for t in texts]


def compute_emotion_distribution(emotions: List[str]) -> Dict[str, float]:
    """Compute % distribution of emotions."""
    if not emotions:
        return {e: 0.0 for e in DISPLAY_LABELS}

    total = len(emotions)
    counts = {e: 0 for e in DISPLAY_LABELS}

    for e in emotions:
        if e in counts:
            counts[e] += 1
        else:
            counts["neutral"] += 1

    return {k: round((v / total) * 100, 1) for k, v in counts.items()}
