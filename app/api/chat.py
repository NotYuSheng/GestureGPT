from fastapi import APIRouter, HTTPException, Request
from app.models.schemas import ChatCompletionRequest, ChatCompletionResponse, ChatCompletionChoice, ChatMessage
from app.services.sign_language_service import get_sign_language_service
from app.services.llm_service import LLMService
import time

router = APIRouter()

# Initialize services
sign_service = get_sign_language_service()
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

        # Generate text response using LLM service
        assistant_response = llm_service.generate_response(request.messages)

        # Lookup sign language videos for the assistant's response
        video_urls, missing_words, normalized_text = sign_service.generate_video(
            assistant_response,
            format=request.format
        )

        # Video URLs from SignASL API are already absolute, no need to prepend base_url
        absolute_video_urls = video_urls

        # Convert user's input to ASL format for suggestion
        _, _, user_input_asl = sign_service.generate_video(
            last_user_message,
            format=request.format
        )

        # Calculate token counts (approximate - based on words in normalized text)
        prompt_tokens = sum(len(msg.content.split()) for msg in request.messages)
        completion_tokens = len(normalized_text.split())

        # Create choice with video URLs
        choice = ChatCompletionChoice(
            index=0,
            message=ChatMessage(
                role="assistant",
                content=assistant_response
            ),
            finish_reason="stop",
            video_urls=absolute_video_urls,
            user_input_asl=user_input_asl
        )

        # Add missing_videos if there are any
        if missing_words:
            choice.missing_videos = missing_words

        # Create response in OpenAI format
        response = ChatCompletionResponse(
            id=f"chatcmpl-{int(time.time())}",
            created=int(time.time()),
            model=request.model,
            choices=[choice],
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
                "id": "gesturegpt-v1",
                "object": "model",
                "created": 1704067200,
                "owned_by": "gesturegpt",
                "permission": [],
                "root": "gesturegpt-v1",
                "parent": None,
            }
        ]
    }
