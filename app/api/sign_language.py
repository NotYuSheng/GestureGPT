from fastapi import APIRouter, HTTPException, Request
from app.models.schemas import SignLanguageRequest, SignLanguageResponse
from app.services.sign_language_service import SignLanguageService
import os

router = APIRouter()
sign_service = SignLanguageService()


@router.post("/generate", response_model=SignLanguageResponse)
async def generate_sign_language(request: SignLanguageRequest, http_request: Request):
    """
    Direct endpoint to convert text to sign language video.

    This endpoint bypasses the LLM and directly converts provided text to sign language.
    """
    try:
        # Generate sign language video
        video_path, duration = sign_service.generate_video(
            request.text,
            format=request.format
        )

        # Convert to relative URL
        video_filename = os.path.basename(video_path)
        base_url = str(http_request.base_url).rstrip('/')
        video_url = f"{base_url}/videos/{video_filename}"

        # Create response
        response = SignLanguageResponse(
            success=True,
            video_url=video_url,
            text=request.text if request.include_subtitles else "",
            format=request.format,
            duration=duration
        )

        return response

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating sign language video: {str(e)}"
        )


@router.get("/video/{filename}")
async def get_video_info(filename: str):
    """
    Get information about a generated video.
    """
    video_path = os.path.join(sign_service.output_dir, filename)

    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video not found")

    info = sign_service.get_video_info(video_path)
    if not info:
        raise HTTPException(status_code=500, detail="Unable to read video information")

    return {
        "filename": filename,
        "exists": True,
        **info
    }
