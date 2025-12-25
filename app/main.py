from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat, sign_language
from app.models.schemas import HealthResponse
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title=os.getenv("API_TITLE", "SignalAPI"),
    version=os.getenv("API_VERSION", "1.0.0"),
    description=os.getenv("API_DESCRIPTION", "Sign Language LLM-style API - Convert text to ASL videos"),
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure output directories exist
os.makedirs("output/videos", exist_ok=True)
os.makedirs("static/videos", exist_ok=True)

# Mount static files for video serving
app.mount("/videos", StaticFiles(directory="output/videos"), name="videos")

# Include routers
app.include_router(chat.router, tags=["Chat Completion (OpenAI-compatible)"])
app.include_router(sign_language.router, prefix="/api/sign-language", tags=["Sign Language"])


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check"""
    return HealthResponse(
        status="healthy",
        version=os.getenv("API_VERSION", "1.0.0"),
        timestamp=datetime.utcnow()
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version=os.getenv("API_VERSION", "1.0.0"),
        timestamp=datetime.utcnow()
    )


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))

    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
