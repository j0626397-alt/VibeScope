"""
Language detection and filtering for English posts.
Uses langdetect library to identify post language before ML processing.
"""

from typing import List, Dict, Tuple
from langdetect import detect, LangDetectException


def is_english(text: str) -> bool:
    """
    Detect if text is in English using langdetect.
    
    Args:
        text: Text to check for English language
        
    Returns:
        True if language is detected as English ("en"), False otherwise
    """
    try:
        return detect(text) == "en"
    except (LangDetectException, Exception):
        # If detection fails, assume not English for safety
        return False


def is_valid_post(post: Dict) -> bool:
    """
    Check if a post meets all filtering criteria:
    1. Text is not empty
    2. Text is at least 3 characters long
    3. Text is in English
    
    Args:
        post: Post dictionary with 'clean_text' key
        
    Returns:
        True if post passes all filters, False otherwise
    """
    clean_text = post.get("clean_text", "").strip()
    
    # Check if text is empty or too short
    if not clean_text or len(clean_text) < 3:
        return False
    
    # Check if text is in English
    if not is_english(clean_text):
        return False
    
    return True


def filter_posts(posts: List[Dict]) -> Tuple[List[Dict], int]:
    """
    Filter posts to keep only valid English posts.
    
    Args:
        posts: List of post dictionaries
        
    Returns:
        Tuple of (filtered_posts, filtered_count)
        - filtered_posts: List of posts that passed all filters
        - filtered_count: Number of posts removed
    """
    original_count = len(posts)
    filtered_posts = [post for post in posts if is_valid_post(post)]
    filtered_count = original_count - len(filtered_posts)
    
    return filtered_posts, filtered_count
