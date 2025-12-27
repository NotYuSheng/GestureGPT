"""
Video Repository Service
Manages ASL video lookups from a JSON index file.
"""

import json
import os
from typing import Dict, List, Optional, Tuple
from pathlib import Path


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
    Loads video mappings from a JSON index file.
    """

    def __init__(self, index_file: str = "data/video_index.json"):
        """
        Initialize the video repository.

        Args:
            index_file: Path to JSON file containing word -> URL mappings
        """
        self.index_file = index_file
        self.index: Dict[str, str] = {}
        self._load_index()

    def _load_index(self) -> None:
        """Load video index from JSON file."""
        if not os.path.exists(self.index_file):
            print(f"Warning: Video index file not found: {self.index_file}")
            print("Creating empty index...")
            self.index = {}
            return

        try:
            with open(self.index_file, 'r') as f:
                self.index = json.load(f)
            print(f"Loaded {len(self.index)} videos from {self.index_file}")
        except json.JSONDecodeError as e:
            print(f"Error loading video index: {e}")
            self.index = {}
        except Exception as e:
            print(f"Unexpected error loading video index: {e}")
            self.index = {}

    def lookup_word(self, word: str) -> Optional[str]:
        """
        Lookup video URL for a single word (case-insensitive).

        Args:
            word: The word to look up

        Returns:
            Video URL if found, None otherwise
        """
        # Normalize to uppercase for case-insensitive lookup
        word_upper = word.upper()
        return self.index.get(word_upper)

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
        Get list of all available videos.

        Returns:
            List of VideoInfo objects
        """
        videos = []
        for word, url in self.index.items():
            # Determine format from URL extension
            format_ext = "mp4"
            if url.endswith(".gif"):
                format_ext = "gif"

            videos.append(VideoInfo(word=word, url=url, format=format_ext))

        return videos

    def get_total_videos(self) -> int:
        """Get total number of videos in repository."""
        return len(self.index)

    def reload_index(self) -> None:
        """Reload video index from disk."""
        self._load_index()

    def word_exists(self, word: str) -> bool:
        """
        Check if a word exists in the repository.

        Args:
            word: Word to check

        Returns:
            True if word exists, False otherwise
        """
        return word.upper() in self.index


# Singleton instance
_repository = None


def get_video_repository() -> VideoRepository:
    """Get singleton instance of VideoRepository."""
    global _repository
    if _repository is None:
        _repository = VideoRepository()
    return _repository
