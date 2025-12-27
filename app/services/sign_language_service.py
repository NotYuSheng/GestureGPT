"""
Sign Language Service
Looks up ASL videos from a repository based on normalized text.
"""

from typing import List, Tuple
from .text_normalizer import get_text_normalizer
from .video_repository import get_video_repository


class SignLanguageService:
    """
    Service for looking up sign language videos from text.

    This service:
    1. Normalizes input text to uppercase word tokens
    2. Looks up corresponding videos from the repository
    3. Returns video URLs and any missing words
    """

    def __init__(self):
        self.normalizer = get_text_normalizer()
        self.repository = get_video_repository()

    def generate_video(self, text: str, format: str = "mp4") -> Tuple[List[str], List[str], str]:
        """
        Lookup videos for the given text.

        Args:
            text: Input text to convert to sign language
            format: Video format (mp4 or gif) - currently only mp4 supported

        Returns:
            Tuple of (video_urls, missing_words, normalized_text)

        Example:
            >>> service = SignLanguageService()
            >>> urls, missing, normalized = service.generate_video("Hello, how are you?")
            >>> print(urls)
            ['/videos/HELLO.mp4', '/videos/HOW.mp4', '/videos/ARE.mp4', '/videos/YOU.mp4']
            >>> print(normalized)
            'HELLO HOW ARE YOU'
        """
        # Normalize text to word tokens
        words = self.normalizer.normalize(text)
        normalized_text = ' '.join(words)

        # Lookup videos from repository
        video_urls, missing_words = self.repository.lookup_words(words)

        return video_urls, missing_words, normalized_text

    def get_available_words(self) -> List[str]:
        """Get list of all words available in the video repository."""
        videos = self.repository.get_all_videos()
        return [video.word for video in videos]

    def get_total_videos(self) -> int:
        """Get total number of videos in the repository."""
        return self.repository.get_total_videos()

    def check_word(self, word: str) -> bool:
        """Check if a word exists in the repository."""
        return self.repository.word_exists(word)


# Singleton instance
_service = None


def get_sign_language_service() -> SignLanguageService:
    """Get singleton instance of SignLanguageService."""
    global _service
    if _service is None:
        _service = SignLanguageService()
    return _service
