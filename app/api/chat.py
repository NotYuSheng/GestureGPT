from fastapi import APIRouter, HTTPException, Request
from app.models.schemas import ChatCompletionRequest, ChatCompletionResponse, ChatCompletionChoice, ChatMessage
from app.services.sign_language_service import SignLanguageService
from app.services.llm_service import LLMService
import time
import os

router = APIRouter()

# Initialize services
sign_service = SignLanguageService()
llm_service = LLMService()


@router.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def create_chat_completion(request: ChatCompletionRequest, http_request: Request):
    """
    OpenAI-compatible chat completion endpoint.

    This endpoint mimics OpenAI's chat API but responds with sign language videos.
    The assistant's text response is also converted to a sign language video.
    """
    try:
        # Validate request
        if request.stream:
            raise HTTPException(status_code=400, detail="Streaming is not supported")

        # Extract the last user message
        user_messages = [msg for msg in request.messages if msg.role == "user"]
        if not user_messages:
            raise HTTPException(status_code=400, detail="No user message found")

        last_user_message = user_messages[-1].content

        # Generate text response using LLM service (placeholder)
        # In production, you could integrate with a real LLM here
        assistant_response = llm_service.generate_response(request.messages)

        # Generate sign language video for the assistant's response
        video_path, duration = sign_service.generate_video(
            assistant_response,
            format=request.format
        )

        # Convert to relative URL
        video_filename = os.path.basename(video_path)
        base_url = str(http_request.base_url).rstrip('/')
        video_url = f"{base_url}/videos/{video_filename}"

        # Calculate token counts (approximate)
        prompt_tokens = sum(len(msg.content.split()) for msg in request.messages)
        completion_tokens = len(assistant_response.split())

        # Create response in OpenAI format
        response = ChatCompletionResponse(
            id=f"chatcmpl-{int(time.time())}",
            created=int(time.time()),
            model=request.model,
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message=ChatMessage(
                        role="assistant",
                        content=assistant_response
                    ),
                    finish_reason="stop",
                    video_url=video_url
                )
            ],
            usage={
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens
            }
        )

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating sign language response: {str(e)}")


@router.get("/v1/models")
async def list_models():
    """
    List available models (OpenAI-compatible endpoint).
    """
    return {
        "object": "list",
        "data": [
            {
                "id": "signalapi-v1",
                "object": "model",
                "created": 1704067200,
                "owned_by": "signalapi",
                "permission": [],
                "root": "signalapi-v1",
                "parent": None,
            }
        ]
    }
