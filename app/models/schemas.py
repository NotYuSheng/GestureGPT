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
    video_urls: List[str] = Field(default_factory=list, description="URLs to sign language videos")
    missing_videos: Optional[List[str]] = Field(None, description="Words without available videos")
    user_input_asl: Optional[str] = Field(None, description="User's input converted to ASL format (text suggestion)")


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
                    "video_urls": [
                        "/videos/HELLO.mp4",
                        "/videos/I.mp4",
                        "/videos/FEEL.mp4",
                        "/videos/GOOD.mp4"
                    ]
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
    video_urls: List[str] = Field(..., description="URLs to access the sign language videos")
    text: str = Field(..., description="Original text")
    normalized_text: str = Field(..., description="Normalized text (uppercase tokens)")
    format: str = Field(..., description="Video format (mp4 or gif)")
    missing_videos: Optional[List[str]] = Field(None, description="Words without available videos")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Generation timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "video_urls": [
                    "/videos/HELLO.mp4",
                    "/videos/HOW.mp4",
                    "/videos/ARE.mp4",
                    "/videos/YOU.mp4"
                ],
                "text": "Hello, how are you?",
                "normalized_text": "HELLO HOW ARE YOU",
                "format": "mp4",
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
    llm_provider: Optional[str] = Field(None, description="LLM provider being used")
    video_repository: str = Field(default="local", description="Video repository type")
    total_videos: int = Field(default=0, description="Total videos available")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Current timestamp")


# Video repository endpoint schemas
class VideoInfo(BaseModel):
    """Information about a single video in the repository"""
    word: str = Field(..., description="The word/sign this video represents")
    url: str = Field(..., description="URL to access the video")
    format: str = Field(default="mp4", description="Video format")


class VideoListResponse(BaseModel):
    """Response for listing all available videos"""
    success: bool = Field(default=True, description="Whether the request was successful")
    total_videos: int = Field(..., description="Total number of videos available")
    videos: List[VideoInfo] = Field(..., description="List of available videos")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "total_videos": 50,
                "videos": [
                    {"word": "HELLO", "url": "/videos/HELLO.mp4", "format": "mp4"},
                    {"word": "WORLD", "url": "/videos/WORLD.mp4", "format": "mp4"}
                ]
            }
        }


class VideoLookupResponse(BaseModel):
    """Response for single word video lookup"""
    success: bool = Field(default=True, description="Whether the request was successful")
    word: str = Field(..., description="The word that was looked up")
    url: str = Field(..., description="URL to access the video")
    format: str = Field(default="mp4", description="Video format")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "word": "HELLO",
                "url": "/videos/HELLO.mp4",
                "format": "mp4"
            }
        }
