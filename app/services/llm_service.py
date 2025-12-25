from typing import List
from app.models.schemas import ChatMessage
import os
from dotenv import load_dotenv

load_dotenv()


class LLMService:
    """
    Service for generating text responses to chat messages.

    Supports multiple LLM providers configured via environment variables:
    - placeholder: Simple canned responses (default)
    - openai: OpenAI GPT models
    - anthropic: Anthropic Claude models
    - custom: Custom OpenAI-compatible endpoint
    """

    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "placeholder").lower()
        self.model_name = "gesturegpt-v1"

        # Initialize provider-specific clients
        self._init_provider()

        # Fallback responses for placeholder mode
        self.responses = {
            "hello": "Hello! I'm doing great, thank you for asking! How can I help you today?",
            "how are you": "I'm doing wonderful! Thanks for asking. How are you doing?",
            "thank you": "You're welcome! I'm happy to help!",
            "bye": "Goodbye! Have a great day!",
            "help": "I'm GestureGPT, a sign language assistant. I respond to your messages in sign language! Ask me anything.",
            "what is your name": "I'm GestureGPT, your sign language assistant!",
            "weather": "I'm sorry, I don't have access to weather information, but I hope it's beautiful where you are!",
        }

    def _init_provider(self):
        """Initialize the selected LLM provider"""
        if self.provider == "openai":
            try:
                import openai
                self.openai_client = openai.OpenAI(
                    api_key=os.getenv("OPENAI_API_KEY"),
                    base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
                )
                self.openai_model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
                print(f"✓ OpenAI provider initialized with model: {self.openai_model}")
            except ImportError:
                print("⚠ OpenAI package not installed. Install with: pip install openai")
                self.provider = "placeholder"
            except Exception as e:
                print(f"⚠ OpenAI initialization failed: {e}")
                self.provider = "placeholder"

        elif self.provider == "anthropic":
            try:
                import anthropic
                self.anthropic_client = anthropic.Anthropic(
                    api_key=os.getenv("ANTHROPIC_API_KEY")
                )
                self.anthropic_model = os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")
                print(f"✓ Anthropic provider initialized with model: {self.anthropic_model}")
            except ImportError:
                print("⚠ Anthropic package not installed. Install with: pip install anthropic")
                self.provider = "placeholder"
            except Exception as e:
                print(f"⚠ Anthropic initialization failed: {e}")
                self.provider = "placeholder"

        elif self.provider == "custom":
            try:
                import openai
                self.custom_client = openai.OpenAI(
                    api_key=os.getenv("CUSTOM_LLM_API_KEY", "not-needed"),
                    base_url=os.getenv("CUSTOM_LLM_ENDPOINT")
                )
                self.custom_model = os.getenv("CUSTOM_LLM_MODEL", "llama2")
                print(f"✓ Custom LLM provider initialized: {os.getenv('CUSTOM_LLM_ENDPOINT')}")
            except ImportError:
                print("⚠ OpenAI package required for custom endpoint. Install with: pip install openai")
                self.provider = "placeholder"
            except Exception as e:
                print(f"⚠ Custom LLM initialization failed: {e}")
                self.provider = "placeholder"

        else:
            print(f"ℹ Using placeholder LLM provider (canned responses)")

    def generate_response(self, messages: List[ChatMessage]) -> str:
        """
        Generate a text response based on conversation history.

        Args:
            messages: List of chat messages in the conversation

        Returns:
            Generated response text
        """
        if self.provider == "openai":
            return self._generate_openai(messages)
        elif self.provider == "anthropic":
            return self._generate_anthropic(messages)
        elif self.provider == "custom":
            return self._generate_custom(messages)
        else:
            return self._generate_placeholder(messages)

    def _generate_openai(self, messages: List[ChatMessage]) -> str:
        """Generate response using OpenAI"""
        try:
            response = self.openai_client.chat.completions.create(
                model=self.openai_model,
                messages=[{"role": m.role, "content": m.content} for m in messages]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"⚠ OpenAI API error: {e}")
            return self._generate_placeholder(messages)

    def _generate_anthropic(self, messages: List[ChatMessage]) -> str:
        """Generate response using Anthropic Claude"""
        try:
            # Convert messages to Anthropic format
            system_messages = [m.content for m in messages if m.role == "system"]
            conversation = [
                {"role": m.role, "content": m.content}
                for m in messages if m.role != "system"
            ]

            response = self.anthropic_client.messages.create(
                model=self.anthropic_model,
                max_tokens=1024,
                system=system_messages[0] if system_messages else None,
                messages=conversation
            )
            return response.content[0].text
        except Exception as e:
            print(f"⚠ Anthropic API error: {e}")
            return self._generate_placeholder(messages)

    def _generate_custom(self, messages: List[ChatMessage]) -> str:
        """Generate response using custom OpenAI-compatible endpoint"""
        try:
            response = self.custom_client.chat.completions.create(
                model=self.custom_model,
                messages=[{"role": m.role, "content": m.content} for m in messages]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"⚠ Custom LLM API error: {e}")
            return self._generate_placeholder(messages)

    def _generate_placeholder(self, messages: List[ChatMessage]) -> str:
        """Generate response using placeholder/canned responses"""
        # Get the last user message
        user_messages = [msg for msg in messages if msg.role == "user"]
        if not user_messages:
            return "Hello! How can I help you today?"

        last_message = user_messages[-1].content.lower().strip()

        # Simple keyword matching for demo purposes
        for keyword, response in self.responses.items():
            if keyword in last_message:
                return response

        # Default response
        if "?" in last_message:
            return f"That's an interesting question! You asked: '{user_messages[-1].content}'. I'll do my best to help!"
        else:
            return f"I understand you said: '{user_messages[-1].content}'. That's great! How else can I assist you?"
