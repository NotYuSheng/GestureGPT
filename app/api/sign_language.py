from fastapi import APIRouter, HTTPException, Request
from app.models.schemas import (
    SignLanguageRequest,
    SignLanguageResponse,
    ErrorResponse,
    VideoListResponse,
    VideoLookupResponse,
    VideoInfo
)
from app.services.sign_language_service import get_sign_language_service

router = APIRouter()
sign_service = get_sign_language_service()


@router.post("/generate", response_model=SignLanguageResponse)
async def generate_sign_language(request: SignLanguageRequest, http_request: Request):
    """
    Direct endpoint to convert text to sign language videos.

    This endpoint bypasses the LLM and directly converts provided text to sign language
    by looking up videos from the repository.

    Returns:
        - 200: Success with video URLs
        - 404: Some or all words not found in repository
    """
    try:
        # Lookup sign language videos
        video_urls, missing_words, normalized_text = sign_service.generate_video(
            request.text,
            format=request.format
        )

        # Convert relative URLs to absolute URLs
        base_url = str(http_request.base_url).rstrip('/')
        absolute_video_urls = [f"{base_url}{url}" for url in video_urls]

        # If there are missing words, return 404 with partial results
        if missing_words:
            return SignLanguageResponse(
                success=False,
                video_urls=absolute_video_urls,
                text=request.text,
                normalized_text=normalized_text,
                format=request.format,
                missing_videos=missing_words
            )

        # Success - all words found
        response = SignLanguageResponse(
            success=True,
            video_urls=absolute_video_urls,
            text=request.text,
            normalized_text=normalized_text,
            format=request.format
        )

        return response

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error looking up sign language videos: {str(e)}"
        )


@router.get("/videos/available", response_model=VideoListResponse)
async def list_available_videos():
    """
    List all available sign language videos in the repository.

    Returns a list of all words/signs that have videos available.
    """
    try:
        videos = sign_service.repository.get_all_videos()

        # Convert VideoInfo objects to dicts
        video_list = [
            VideoInfo(
                word=video.word,
                url=video.url,
                format=video.format
            )
            for video in videos
        ]

        return VideoListResponse(
            success=True,
            total_videos=len(video_list),
            videos=video_list
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving video list: {str(e)}"
        )


@router.get("/videos/lookup/{word}")
async def lookup_word_video(word: str, http_request: Request):
    """
    Lookup video URL for a specific word.

    Args:
        word: The word to look up (case-insensitive)

    Returns:
        - 200: Video found
        - 404: Video not found
    """
    try:
        video_url = sign_service.repository.lookup_word(word)

        if video_url is None:
            return ErrorResponse(
                success=False,
                error="Video not found",
                detail=f"No video available for sign: {word.upper()}"
            )

        # Convert relative URL to absolute URL
        base_url = str(http_request.base_url).rstrip('/')
        absolute_url = f"{base_url}{video_url}"

        # Determine format from URL
        format_ext = "mp4"
        if video_url.endswith(".gif"):
            format_ext = "gif"

        return VideoLookupResponse(
            success=True,
            word=word.upper(),
            url=absolute_url,
            format=format_ext
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error looking up video: {str(e)}"
        )
