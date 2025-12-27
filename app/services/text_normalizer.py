"""
Text Normalizer Service
Converts text into normalized ASL word tokens for video lookup.
"""

import re
from typing import List
import nltk
from nltk.tokenize import word_tokenize


class TextNormalizer:
    """
    Normalizes text for ASL video lookup.
    Converts input text to uppercase word tokens suitable for sign language.
    """

    def __init__(self):
        """Initialize the text normalizer and download required NLTK data."""
        self._ensure_nltk_data()

    def _ensure_nltk_data(self):
        """Download NLTK punkt tokenizer if not already present."""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            print("Downloading NLTK punkt tokenizer...")
            nltk.download('punkt', quiet=True)

    def normalize(self, text: str) -> List[str]:
        """
        Normalize text to ASL word tokens.

        Process:
        1. Tokenize using NLTK word_tokenize
        2. Convert to uppercase
        3. Remove punctuation and special characters
        4. Filter out empty strings

        Args:
            text: Input text to normalize

        Returns:
            List of uppercase word tokens

        Example:
            >>> normalizer = TextNormalizer()
            >>> normalizer.normalize("Hello, how are you?")
            ['HELLO', 'HOW', 'ARE', 'YOU']
        """
        if not text or not text.strip():
            return []

        # Tokenize using NLTK
        tokens = word_tokenize(text)

        # Process tokens
        normalized_tokens = []
        for token in tokens:
            # Convert to uppercase
            token = token.upper()

            # Remove punctuation and special characters, keep only alphanumeric
            token = re.sub(r'[^A-Z0-9]', '', token)

            # Add non-empty tokens
            if token:
                normalized_tokens.append(token)

        return normalized_tokens

    def normalize_to_string(self, text: str) -> str:
        """
        Normalize text and return as space-separated string.

        Args:
            text: Input text to normalize

        Returns:
            Space-separated uppercase tokens

        Example:
            >>> normalizer = TextNormalizer()
            >>> normalizer.normalize_to_string("Hello, how are you?")
            'HELLO HOW ARE YOU'
        """
        tokens = self.normalize(text)
        return ' '.join(tokens)


# Singleton instance
_normalizer = None


def get_text_normalizer() -> TextNormalizer:
    """Get singleton instance of TextNormalizer."""
    global _normalizer
    if _normalizer is None:
        _normalizer = TextNormalizer()
    return _normalizer
