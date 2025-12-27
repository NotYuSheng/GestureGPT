"""
Video Repository Service
Manages ASL video lookups from SignASL API with local caching.
"""

import json
import os
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from app.services.signasl_client import get_signasl_client


class VideoInfo:
    """Information about a video in the repository."""

    def __init__(self, word: str, url: str, format: str = "mp4"):
        self.word = word
        self.url = url
        self.format = format

    def to_dict(self) -> dict:
        return {
            "word": self.word,
            "url": self.url,
            "format": self.format
        }


class VideoRepository:
    """
    Repository for ASL video lookups.
    Uses SignASL API with local caching for performance.
    """

    def __init__(self, cache_file: str = "data/video_cache.json"):
        """
        Initialize the video repository.

        Args:
            cache_file: Path to JSON file for caching video URLs
        """
        self.cache_file = cache_file
        self.cache: Dict[str, str] = {}
        self.signasl = get_signasl_client()
        self._load_cache()

    def _load_cache(self) -> None:
        """Load video cache from JSON file."""
        if not os.path.exists(self.cache_file):
            print(f"Video cache not found, starting fresh")
            self.cache = {}
            return

        try:
            with open(self.cache_file, 'r') as f:
                self.cache = json.load(f)
            print(f"Loaded {len(self.cache)} cached videos from {self.cache_file}")
        except json.JSONDecodeError as e:
            print(f"Error loading video cache: {e}")
            self.cache = {}
        except Exception as e:
            print(f"Unexpected error loading video cache: {e}")
            self.cache = {}

    def _save_cache(self) -> None:
        """Save video cache to JSON file."""
        try:
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            print(f"Error saving video cache: {e}")

    def lookup_word(self, word: str) -> Optional[str]:
        """
        Lookup video URL for a single word (case-insensitive).
        Checks cache first, then fetches from SignASL API if needed.

        Args:
            word: The word to look up

        Returns:
            Video URL if found, None otherwise
        """
        # Normalize to uppercase for case-insensitive lookup
        word_upper = word.upper()

        # Check cache first
        if word_upper in self.cache:
            return self.cache[word_upper]

        # Fetch from SignASL API
        url = self.signasl.get_video_url(word)
        if url:
            # Cache the result
            self.cache[word_upper] = url
            self._save_cache()
            return url

        return None

    def lookup_words(self, words: List[str]) -> Tuple[List[str], List[str]]:
        """
        Lookup multiple words.

        Args:
            words: List of words to look up

        Returns:
            Tuple of (found_video_urls, missing_words)
        """
        found_urls = []
        missing_words = []

        for word in words:
            url = self.lookup_word(word)
            if url:
                found_urls.append(url)
            else:
                missing_words.append(word)

        return found_urls, missing_words

    def get_all_videos(self) -> List[VideoInfo]:
        """
        Get list of all cached videos.

        Returns:
            List of VideoInfo objects
        """
        videos = []
        for word, url in self.cache.items():
            # Determine format from URL extension
            format_ext = "mp4"
            if url.endswith(".gif"):
                format_ext = "gif"

            videos.append(VideoInfo(word=word, url=url, format=format_ext))

        return videos

    def get_total_videos(self) -> int:
        """Get total number of cached videos."""
        return len(self.cache)

    def reload_cache(self) -> None:
        """Reload video cache from disk."""
        self._load_cache()

    def clear_cache(self) -> None:
        """Clear the video cache."""
        self.cache = {}
        self._save_cache()

    def word_exists(self, word: str) -> bool:
        """
        Check if a word exists in the cache.
        Note: This doesn't check SignASL API, only the local cache.

        Args:
            word: Word to check

        Returns:
            True if word exists in cache, False otherwise
        """
        return word.upper() in self.cache


# Singleton instance
_repository = None


def get_video_repository() -> VideoRepository:
    """Get singleton instance of VideoRepository."""
    global _repository
    if _repository is None:
        _repository = VideoRepository()
    return _repository
