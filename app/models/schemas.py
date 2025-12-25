from pydantic import BaseModel, Field
from typing import Optional, Literal, List, Dict, Any
from datetime import datetime


# OpenAI-compatible schemas
class ChatMessage(BaseModel):
    """Chat message in OpenAI format"""
    role: Literal["system", "user", "assistant"] = Field(..., description="Role of the message sender")
    content: str = Field(..., description="Content of the message")


class ChatCompletionRequest(BaseModel):
    """OpenAI-compatible chat completion request"""
    model: str = Field(default="signalapi-v1", description="Model identifier")
    messages: List[ChatMessage] = Field(..., min_length=1, description="List of messages in the conversation")
    temperature: Optional[float] = Field(default=1.0, ge=0, le=2, description="Sampling temperature (ignored)")
    max_tokens: Optional[int] = Field(default=None, description="Maximum tokens (ignored)")
    stream: bool = Field(default=False, description="Stream response (not supported)")
    format: Literal["mp4", "gif"] = Field(default="mp4", description="Video format for sign language response")

    class Config:
        json_schema_extra = {
            "example": {
                "model": "signalapi-v1",
                "messages": [
                    {"role": "user", "content": "Hello, how are you?"}
                ],
                "format": "mp4"
            }
        }


class ChatCompletionChoice(BaseModel):
    """Choice in chat completion response"""
    index: int = Field(..., description="Choice index")
    message: ChatMessage = Field(..., description="Response message")
    finish_reason: str = Field(default="stop", description="Reason for completion finish")
    video_url: Optional[str] = Field(None, description="URL to sign language video")


class ChatCompletionUsage(BaseModel):
    """Token usage information (compatibility)"""
    prompt_tokens: int = Field(default=0, description="Tokens in prompt")
    completion_tokens: int = Field(default=0, description="Tokens in completion")
    total_tokens: int = Field(default=0, description="Total tokens used")


class ChatCompletionResponse(BaseModel):
    """OpenAI-compatible chat completion response"""
    id: str = Field(..., description="Unique completion ID")
    object: str = Field(default="chat.completion", description="Object type")
    created: int = Field(..., description="Unix timestamp of creation")
    model: str = Field(..., description="Model used")
    choices: List[ChatCompletionChoice] = Field(..., description="List of completion choices")
    usage: ChatCompletionUsage = Field(default_factory=ChatCompletionUsage, description="Token usage stats")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "chatcmpl-123",
                "object": "chat.completion",
                "created": 1677652288,
                "model": "signalapi-v1",
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "Hello! I feel good. Thank you ask!"
                    },
                    "finish_reason": "stop",
                    "video_url": "/videos/sign_abc123_1234567890.mp4"
                }],
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 15,
                    "total_tokens": 25
                }
            }
        }


# Direct sign language endpoint schemas
class SignLanguageRequest(BaseModel):
    """Request model for sign language video generation"""
    text: str = Field(..., min_length=1, max_length=500, description="Text to convert to sign language")
    format: Literal["mp4", "gif"] = Field(default="mp4", description="Output video format")
    include_subtitles: bool = Field(default=True, description="Include text subtitles in response")

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Hello, how are you?",
                "format": "mp4",
                "include_subtitles": True
            }
        }


class SignLanguageResponse(BaseModel):
    """Response model for sign language video generation"""
    success: bool = Field(..., description="Whether the request was successful")
    video_url: str = Field(..., description="URL to access the generated video")
    text: str = Field(..., description="Original text for subtitles")
    format: str = Field(..., description="Video format (mp4 or gif)")
    duration: Optional[float] = Field(None, description="Video duration in seconds")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Generation timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "video_url": "/videos/hello_how_are_you_1234567890.mp4",
                "text": "Hello, how are you?",
                "format": "mp4",
                "duration": 3.5,
                "timestamp": "2024-01-15T10:30:00"
            }
        }


class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = Field(default=False, description="Always false for errors")
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Current timestamp")
