"""
SignASL API Client
Fetches video URLs from the SignASL scraper API.
"""

import os
import requests
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class SignASLClient:
    """Client for interacting with SignASL API."""

    def __init__(self):
        self.base_url = os.getenv("SIGNASL_API_URL", "http://signasl-api:8001")
        self.timeout = 10

    def get_video_url(self, word: str) -> Optional[str]:
        """
        Get video URL for a word from SignASL API.

        Args:
            word: The word to get video for

        Returns:
            Video URL if found, None otherwise
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/video-url/{word}",
                timeout=self.timeout
            )

            if response.status_code == 200:
                data = response.json()
                # SignASL API returns {"word": "hello", "video_urls": ["https://...", ...]}
                # Get the first video URL from the array
                video_urls = data.get("video_urls", [])
                return video_urls[0] if video_urls else None
            elif response.status_code == 404:
                return None
            else:
                print(f"⚠ SignASL API returned status {response.status_code} for word: {word}")
                return None

        except requests.exceptions.Timeout:
            print(f"⚠ SignASL API timeout for word: {word}")
            return None
        except requests.exceptions.ConnectionError:
            print(f"⚠ Cannot connect to SignASL API at {self.base_url}")
            return None
        except Exception as e:
            print(f"⚠ SignASL API error for word '{word}': {e}")
            return None

    def health_check(self) -> bool:
        """
        Check if SignASL API is available.

        Returns:
            True if API is healthy, False otherwise
        """
        try:
            response = requests.get(
                f"{self.base_url}/health",
                timeout=self.timeout
            )
            return response.status_code == 200
        except:
            return False


# Singleton instance
_client = None


def get_signasl_client() -> SignASLClient:
    """Get singleton instance of SignASLClient."""
    global _client
    if _client is None:
        _client = SignASLClient()
    return _client
