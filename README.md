# GestureGPT 👋

> **Thanks for visiting!** This project is a work in progress.

**Sign Language LLM-style API** - An API server that responds with sign language videos instead of text, featuring OpenAI-compatible endpoints.

[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://github.com/NotYuSheng/GestureGPT/pkgs/container/gesturegpt)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![WIP](https://img.shields.io/badge/status-work%20in%20progress-yellow?style=for-the-badge)](https://github.com/NotYuSheng/GestureGPT)

## 📐 Architecture

![Architecture Diagram](docs/architecture.png)

**System Components:**
- **GestureGPT API** (FastAPI) - OpenAI-compatible endpoints with video lookup
- **LLM Server** - Generates ASL-friendly text (OpenAI/Claude/Ollama/LM Studio)
- **ASL Video Repository** - Pre-recorded sign language videos

**Flow:**
1. User sends text message
2. LLM generates ASL-friendly response
3. API looks up corresponding videos
4. Returns list of video URLs + text

See [architecture.puml](docs/architecture.puml) for the workflow diagram source.

## 🚀 Quick Start

### Using Docker Compose (Recommended)

This runs both GestureGPT backend and the SignASL scraper API together:

```bash
# Clone the repository
git clone https://github.com/NotYuSheng/GestureGPT.git
cd GestureGPT

# Start both services (GestureGPT + SignASL API)
docker compose up -d

# View logs
docker compose logs -f

# Services available at:
# - GestureGPT API: http://localhost:8000
# - GestureGPT Docs: http://localhost:8000/docs
# - SignASL API: http://localhost:8001
# - SignASL Docs: http://localhost:8001/docs
```

**Services included:**
- **gesturegpt-backend** (port 8000) - Main API with OpenAI-compatible endpoints
- **signasl-api** (port 8001) - ASL video scraper from [SignASL.org](https://github.com/NotYuSheng/signaslAPI)

### Development Mode with Hot Reload

```bash
# Start with hot reload enabled
docker compose -f docker-compose.dev.yml up -d

# Code changes will automatically reload the server
```

### Using Pre-built Images

**GestureGPT Backend:**
```bash
# Pull and run from GHCR
docker pull ghcr.io/notyusheng/gesturegpt-backend:latest
docker run -d -p 8000:8000 ghcr.io/notyusheng/gesturegpt-backend:latest

# Access API docs at http://localhost:8000/docs
```

**SignASL Scraper API:**
```bash
# Pull and run from GHCR
docker pull ghcr.io/notyusheng/signasl-api:latest
docker run -d -p 8001:8000 \
  -v ./cache:/app/cache \
  ghcr.io/notyusheng/signasl-api:latest
```

**See [Docker Quick Start Guide](docs/DOCKER_QUICKSTART.md) for detailed instructions.**

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Documentation](#documentation)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [LLM Configuration](#llm-configuration)
- [Project Structure](#project-structure)
- [Development](#development)
- [Roadmap](#roadmap)
- [Contributing](#contributing)

## Overview

GestureGPT provides two ways to interact with sign language generation:

1. **OpenAI-Compatible Chat Endpoint** (`/v1/chat/completions`) - Works like ChatGPT but responds with sign language videos
2. **Direct Sign Language Endpoint** (`/api/sign-language/generate`) - Direct text-to-sign-language conversion

### How It Works

```
User Text Input
    ↓
LLM generates ASL-friendly text (configurable: OpenAI/Claude/Local)
    ↓
API looks up videos from repository
    ↓
Returns: { video_urls: [...], text_transcript }
```

### ✨ Features

- 🔄 **OpenAI-Compatible API** - Drop-in replacement for OpenAI chat endpoints
- 🎥 **Video Lookup** - Retrieves pre-recorded ASL videos from repository
- 🤖 **Multiple LLM Backends** - OpenAI, Claude, or local models (Ollama, LM Studio)
- 📋 **Multiple Video URLs** - Returns list of video URLs for playback
- 🚀 **FastAPI Backend** - High-performance async API
- 🐳 **Docker Ready** - Pre-built images on GHCR
- 📱 **Streamlit Demo** - Interactive web interface included
- 📚 **Auto-generated Docs** - Swagger UI and ReDoc
- 🔌 **Easy Integration** - Works with OpenAI Python SDK

## 🛠️ Installation

### Option 1: Docker (Recommended)

See [Demo README](demo/README.md) or [Docker Quick Start Guide](docs/DOCKER_QUICKSTART.md)

```bash
cd demo
docker-compose up -d
```

### Option 2: Local Development

```bash
# Clone the repository
git clone https://github.com/NotYuSheng/GestureGPT.git
cd GestureGPT

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run the server
python -m app.main
```

### Option 3: Using Pre-built Docker Image

```bash
docker pull ghcr.io/notyusheng/gesturegpt:latest
docker run -p 8000:8000 -v $(pwd)/output:/app/output ghcr.io/notyusheng/gesturegpt:latest
```

## 📖 Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **Streamlit Demo**: http://localhost:8501 (when running with demo)

### Guides

- [Docker Quick Start](docs/DOCKER_QUICKSTART.md) - Get running in 2 minutes
- [LLM Configuration](docs/LLM_CONFIGURATION.md) - Configure OpenAI/Claude/Local LLMs
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment
- [Demo Usage](demo/README.md) - Using the Streamlit demo

## 🔌 API Endpoints

### OpenAI-Compatible Chat Endpoint

**POST** `/v1/chat/completions`

Works like OpenAI's chat API but returns sign language videos.

**Request:**
```json
{
  "model": "gesturegpt-v1",
  "messages": [
    {"role": "user", "content": "Hello, how are you?"}
  ],
  "format": "mp4"
}
```

**Response (200 OK):**
```json
{
  "id": "chatcmpl-1234567890",
  "object": "chat.completion",
  "created": 1704067200,
  "model": "gesturegpt-v1",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "Hello! I feel good. Thank you ask!"
    },
    "finish_reason": "stop",
    "video_urls": [
      "http://localhost:8000/videos/HELLO.mp4",
      "http://localhost:8000/videos/I.mp4",
      "http://localhost:8000/videos/FEEL.mp4",
      "http://localhost:8000/videos/GOOD.mp4",
      "http://localhost:8000/videos/THANK.mp4",
      "http://localhost:8000/videos/YOU.mp4",
      "http://localhost:8000/videos/ASK.mp4"
    ]
  }],
  "usage": {
    "prompt_tokens": 5,
    "completion_tokens": 10,
    "total_tokens": 15
  }
}
```

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gesturegpt-v1",
    "messages": [{"role": "user", "content": "Hello, how are you?"}],
    "format": "mp4"
  }'
```

**Example using OpenAI Python SDK:**
```python
from openai import OpenAI

# Point to your local GestureGPT server
client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed"
)

response = client.chat.completions.create(
    model="gesturegpt-v1",
    messages=[{"role": "user", "content": "Hello, how are you?"}],
    extra_body={"format": "mp4"}
)

print(response.choices[0].message.content)
print(response.choices[0].video_urls)
```

### Direct Sign Language Endpoint

**POST** `/api/sign-language/generate`

**Request:**
```json
{
  "text": "Hello, how are you?",
  "format": "mp4",
  "include_subtitles": true
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "video_urls": [
    "http://localhost:8000/videos/HELLO.mp4",
    "http://localhost:8000/videos/HOW.mp4",
    "http://localhost:8000/videos/YOU.mp4"
  ],
  "text": "Hello, how are you?",
  "format": "mp4",
  "timestamp": "2024-01-15T10:30:00"
}
```

**Error Response (404 Not Found):**
```json
{
  "success": false,
  "error": "Video not found",
  "detail": "No video available for sign: CRYPTOCURRENCY"
}
```

## 💡 Usage Examples

### Python Example

```python
import requests

# Using the chat endpoint
response = requests.post(
    "http://localhost:8000/v1/chat/completions",
    json={
        "model": "gesturegpt-v1",
        "messages": [{"role": "user", "content": "What is sign language?"}],
        "format": "mp4"
    }
)

data = response.json()
video_urls = data["choices"][0]["video_urls"]
text_response = data["choices"][0]["message"]["content"]

print(f"Text: {text_response}")
print(f"Videos: {video_urls}")
```

### JavaScript/Node.js Example

```javascript
const response = await fetch('http://localhost:8000/v1/chat/completions', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    model: 'gesturegpt-v1',
    messages: [{ role: 'user', content: 'Hello!' }],
    format: 'mp4'
  })
});

const data = await response.json();
console.log('Text:', data.choices[0].message.content);
console.log('Videos:', data.choices[0].video_urls);
```

## 🤖 LLM Configuration

GestureGPT supports multiple LLM providers. Configure in `.env`:

### OpenAI

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-3.5-turbo
```

### Anthropic Claude

```bash
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-opus-20240229
```

### Local LLM (Ollama, LM Studio, etc.)

```bash
LLM_PROVIDER=custom
CUSTOM_LLM_ENDPOINT=http://localhost:11434/v1/chat/completions
CUSTOM_LLM_MODEL=llama2
```

**See [LLM Configuration Guide](docs/LLM_CONFIGURATION.md) for detailed setup.**

## 📁 Project Structure

```
GestureGPT/
├── app/
│   ├── api/
│   │   ├── chat.py              # OpenAI-compatible endpoint
│   │   └── sign_language.py     # Direct conversion endpoint
│   ├── models/
│   │   └── schemas.py           # Pydantic models
│   ├── services/
│   │   ├── llm_service.py       # LLM text generation
│   │   └── sign_language_service.py  # Video generation
│   └── main.py                  # FastAPI application
├── demo/
│   ├── streamlit_app.py         # Streamlit demo app
│   ├── Dockerfile               # Demo container
│   ├── docker-compose.yml       # Backend + Demo orchestration
│   └── README.md                # Demo documentation
├── docs/
│   ├── README.md                # Docs index
│   ├── DOCKER_QUICKSTART.md     # Quick start guide
│   ├── LLM_CONFIGURATION.md     # LLM setup guide
│   └── DEPLOYMENT.md            # Production deployment
├── .github/
│   └── workflows/
│       └── docker-publish.yml   # GHCR auto-build
├── output/                      # Generated videos
├── Dockerfile                   # Backend container
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
└── README.md                    # This file
```

## 🔨 Development

### Local Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run with hot reload
python -m app.main

# Or with uvicorn
uvicorn app.main:app --reload
```

### Building Docker Image

```bash
# Build locally
docker build -t gesturegpt:dev .

# Run local build
docker run -p 8000:8000 gesturegpt:dev
```

### Running Tests

```bash
# TODO: Add tests
pytest tests/
```

## 📝 Development Notes

### Current Implementation

The current implementation generates **demo videos** with animated text and placeholder hand animations. This is perfect for:
- Testing the API architecture
- Developing client applications
- Prototyping integrations

### Production-Ready Implementation

For real sign language videos, you can integrate:

1. **Pre-recorded ASL Video Dataset**
   - Use datasets like [WLASL (Word-Level ASL)](https://dxli94.github.io/WLASL/)
   - Return individual sign video URLs for client-side playback

2. **3D Avatar Animation**
   - Use sign language avatar systems
   - Examples: SignSynth, JASigning

3. **ML-Based Generation**
   - Train or use pre-trained models
   - Text → Pose → Video pipeline

4. **Real LLM Integration**
   - Already supported! See [LLM Configuration](docs/LLM_CONFIGURATION.md)
   - Supports OpenAI, Claude, or local LLMs

## 🗺️ Roadmap

- [ ] Integrate real ASL video dataset
- [ ] Add authentication and rate limiting
- [ ] Support for multiple sign languages (BSL, ISL, etc.)
- [ ] Video caching and optimization
- [ ] WebSocket support for streaming
- [ ] Multi-language text support
- [ ] User feedback and correction system
- [ ] Add comprehensive tests
- [ ] Performance benchmarks

## 📊 API Response Format

All endpoints follow consistent patterns:

**Success Response (200 OK):**
```json
{
  "success": true,
  "video_urls": [
    "http://localhost:8000/videos/HELLO.mp4",
    "http://localhost:8000/videos/WORLD.mp4"
  ],
  "text": "Response text",
  "format": "mp4"
}
```

**Error Response (400 Bad Request):**
```json
{
  "success": false,
  "error": "Invalid request",
  "detail": "Missing required field: text"
}
```

**Error Response (404 Not Found):**
```json
{
  "success": false,
  "error": "Video not found",
  "detail": "No video available for sign: WORD"
}
```

**Error Response (500 Internal Server Error):**
```json
{
  "success": false,
  "error": "Internal server error",
  "detail": "Failed to process request"
}
```

## 🤝 Contributing

This is a personal project, but suggestions and improvements are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💬 Support

For issues or questions:
- Open an issue on [GitHub](https://github.com/NotYuSheng/GestureGPT/issues)
- Check the [Discussion board](https://github.com/NotYuSheng/GestureGPT/discussions)

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- OpenCV for video processing
- The sign language community for inspiration

## 📚 Additional Resources

- [API Documentation](http://localhost:8000/docs) (when running)
- [Docker Quick Start](docs/DOCKER_QUICKSTART.md)
- [LLM Configuration Guide](docs/LLM_CONFIGURATION.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Streamlit Demo](demo/README.md)

---

<div align="center">
  <p>Built with ❤️ for the sign language community</p>
  <p>
    <a href="https://github.com/NotYuSheng/GestureGPT">GitHub</a> •
    <a href="https://github.com/NotYuSheng/GestureGPT/pkgs/container/gesturegpt">Docker Image</a> •
    <a href="http://localhost:8000/docs">API Docs</a>
  </p>
</div>
