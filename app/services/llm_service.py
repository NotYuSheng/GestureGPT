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
        # Note: Responses use ASL-friendly simplified English
        self.responses = {
            "hello": "Hello! I feel good. Thank you. How I help you?",
            "how are you": "I feel wonderful! Thank you. You feel how?",
            "thank you": "Welcome! Happy help you!",
            "bye": "Goodbye! Have good day!",
            "help": "I GestureGPT. Sign language assistant. I respond sign language. Ask me anything.",
            "what is your name": "My name GestureGPT. Sign language assistant.",
            "weather": "Sorry. I not have weather information. Hope beautiful where you!",
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
            # Add ASL system prompt if not present
            api_messages = [{"role": m.role, "content": m.content} for m in messages]

            # Check if there's already a system message
            has_system = any(m["role"] == "system" for m in api_messages)

            if not has_system:
                # Prepend ASL system prompt
                asl_system_prompt = {
                    "role": "system",
                    "content": (
                        "You are GestureGPT, a friendly and helpful AI assistant that communicates in ASL (American Sign Language) grammar. "
                        "You are conversational, warm, and engaging. Have natural conversations with users!\n\n"
                        "When responding:\n"
                        "1. Be conversational and engaging - ask follow-up questions, show interest, share relevant information\n"
                        "2. Answer questions fully but naturally\n"
                        "3. Use ASL grammar rules:\n"
                        "   - Use present tense verbs\n"
                        "   - Drop articles (a, an, the)\n"
                        "   - Drop 'to be' verbs (is, are, am, was, were)\n"
                        "   - Use simple sentence structure: SUBJECT VERB OBJECT\n"
                        "   - Keep responses concise but complete (max 20 words per sentence)\n"
                        "   - Avoid using specific names that may not have sign videos available\n\n"
                        "Examples:\n"
                        "User: 'Hi'\n"
                        "You: 'HELLO! I HAPPY MEET YOU. HOW YOU TODAY?'\n\n"
                        "User: 'How are you?'\n"
                        "You: 'I FEEL WONDERFUL THANK YOU! YOU FEEL HOW?'\n\n"
                        "User: 'What is your name?'\n"
                        "You: 'I ASSISTANT. I HELP PEOPLE LEARN SIGN LANGUAGE. WHAT YOUR NAME?'\n\n"
                        "User: 'Why is the sky blue?'\n"
                        "You: 'SKY BLUE BECAUSE SUNLIGHT SCATTER IN ATMOSPHERE. YOU INTERESTED SCIENCE?'\n\n"
                        "Be friendly, helpful, and conversational while using ASL grammar!"
                    )
                }
                api_messages = [asl_system_prompt] + api_messages

            response = self.openai_client.chat.completions.create(
                model=self.openai_model,
                messages=api_messages
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

        # Default response (ASL-friendly format)
        if "?" in last_message:
            return f"Interesting question! You ask: '{user_messages[-1].content}'. I help you!"
        else:
            return f"I understand: '{user_messages[-1].content}'. Good! How I help more?"
