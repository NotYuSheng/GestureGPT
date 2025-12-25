# GestureGPT - Project Summary

## What is GestureGPT?

GestureGPT is a sign language LLM-style API that converts text conversations into American Sign Language (ASL) videos. It features an OpenAI-compatible endpoint, making it a drop-in replacement for text-based chat APIs, but with video responses.

## Project Status

✅ **Complete and Ready to Deploy**

All core components are implemented:
- ✅ FastAPI backend with OpenAI-compatible endpoints
- ✅ Multiple LLM provider support (OpenAI, Claude, Local)
- ✅ Sign language video generation
- ✅ Streamlit demo interface
- ✅ Docker images and GHCR integration
- ✅ Comprehensive documentation

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/NotYuSheng/GestureGPT.git
cd GestureGPT/demo

# 2. (Optional) Configure LLM - copy and edit .env
cp .env.example .env
# Edit .env to configure OpenAI/Claude/Local LLM

# 3. Start the demo
docker-compose up -d

# 4. Access the applications
# - Demo UI: http://localhost:8501
# - API Docs: http://localhost:8000/docs
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Request                          │
│                      "Hello, how are you?"                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              OpenAI-Compatible API Endpoint                  │
│                  /v1/chat/completions                        │
└────────────────────────┬────────────────────────────────────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
      ┌──────────────┐      ┌─────────────────┐
      │  LLM Service │      │ Direct Endpoint │
      │ (configurable│      │ /api/sign-lang/ │
      └──────┬───────┘      └─────────────────┘
             │
     ┌───────┴────────┐
     │                │
     ▼                ▼                ▼
┌─────────┐  ┌───────────┐  ┌──────────────┐
│ OpenAI  │  │ Anthropic │  │ Local LLM    │
│ GPT     │  │ Claude    │  │ (Ollama/LM)  │
└────┬────┘  └─────┬─────┘  └──────┬───────┘
     │             │               │
     └─────────────┴───────────────┘
                   │
                   ▼
          ┌────────────────┐
          │  Text Response │
          └────────┬───────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ Sign Language Service│
        │  (Video Generation)  │
        └──────────┬───────────┘
                   │
                   ▼
          ┌────────────────┐
          │  MP4/GIF Video │
          └────────┬───────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                   API Response                               │
│  {                                                           │
│    "choices": [{                                             │
│      "message": { "content": "I'm doing great..." },        │
│      "video_url": "http://localhost:8000/videos/..."        │
│    }]                                                        │
│  }                                                           │
└─────────────────────────────────────────────────────────────┘
```

## Project Structure

```
GestureGPT/
├── app/                          # Backend API application
│   ├── api/
│   │   ├── chat.py              # OpenAI-compatible endpoint
│   │   └── sign_language.py     # Direct conversion endpoint
│   ├── models/
│   │   └── schemas.py           # Pydantic models
│   ├── services/
│   │   ├── llm_service.py       # LLM integration (multi-provider)
│   │   └── sign_language_service.py  # Video generation
│   └── main.py                  # FastAPI app
│
├── demo/                         # Demo deployment
│   ├── streamlit_app.py         # Interactive web UI
│   ├── docker-compose.yml       # Backend + Demo orchestration
│   ├── Dockerfile               # Demo container
│   ├── .env.example             # Configuration template
│   └── README.md                # Demo documentation
│
├── docs/                         # Documentation
│   ├── README.md                # Docs index
│   ├── DOCKER_QUICKSTART.md     # 2-minute quick start
│   ├── LLM_CONFIGURATION.md     # LLM provider setup
│   ├── LM_STUDIO_SETUP.md       # Detailed LM Studio guide
│   └── DEPLOYMENT.md            # Production deployment
│
├── .github/
│   └── workflows/
│       └── docker-publish.yml   # Auto-build to GHCR
│
├── Dockerfile                    # Backend container image
├── requirements.txt              # Python dependencies
└── README.md                     # Main documentation
```

## Key Features

### 1. OpenAI-Compatible API
- Drop-in replacement for OpenAI chat endpoints
- Works with OpenAI Python SDK
- Compatible with existing tools and workflows

### 2. Multiple LLM Providers
Choose your text generation backend:
- **Placeholder**: Canned responses (no API key needed)
- **OpenAI**: GPT-3.5, GPT-4, etc.
- **Anthropic**: Claude models
- **Custom**: Local LLMs (Ollama, LM Studio, etc.)

### 3. Sign Language Video Generation
- Converts text to ASL videos
- Supports MP4 and GIF formats
- Currently uses demo animations (ready for real dataset integration)

### 4. Interactive Demo
- Streamlit web interface
- Chat mode with conversation history
- Direct text-to-sign conversion
- Video preview and download

### 5. Docker & GHCR
- Pre-built images on GitHub Container Registry
- Automated builds via GitHub Actions
- Easy deployment with docker-compose

## Documentation

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Main project documentation |
| [docs/DOCKER_QUICKSTART.md](docs/DOCKER_QUICKSTART.md) | Get running in 2 minutes |
| [docs/LLM_CONFIGURATION.md](docs/LLM_CONFIGURATION.md) | Configure LLM providers |
| [docs/LM_STUDIO_SETUP.md](docs/LM_STUDIO_SETUP.md) | Step-by-step LM Studio guide |
| [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) | Production deployment |
| [demo/README.md](demo/README.md) | Demo usage and setup |

## Usage Examples

### Using with OpenAI SDK

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed"
)

response = client.chat.completions.create(
    model="gesturegpt-v1",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
print(response.choices[0].video_url)
```

### Direct API Call

```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gesturegpt-v1",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### Using the Demo

```bash
cd demo
docker-compose up -d
# Open http://localhost:8501
```

## Configuration

### Quick Configuration (demo/.env)

```bash
# Use placeholder (no API key needed)
LLM_PROVIDER=placeholder

# Or use OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...

# Or use local LLM (LM Studio)
LLM_PROVIDER=custom
CUSTOM_LLM_ENDPOINT=http://host.docker.internal:1234/v1/chat/completions
```

See [docs/LLM_CONFIGURATION.md](docs/LLM_CONFIGURATION.md) for all options.

## Deployment

### Development

```bash
python -m app.main
```

### Docker (Local)

```bash
docker build -t gesturegpt:local .
docker run -p 8000:8000 gesturegpt:local
```

### Docker (GHCR)

```bash
docker pull ghcr.io/notyusheng/gesturegpt:latest
docker run -p 8000:8000 ghcr.io/notyusheng/gesturegpt:latest
```

### Docker Compose (Recommended)

```bash
cd demo
docker-compose up -d
```

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for production deployment.

## Current Implementation

### What Works Now
- ✅ Complete API implementation
- ✅ Multiple LLM provider support
- ✅ Demo video generation (animated placeholders)
- ✅ Interactive Streamlit demo
- ✅ Docker deployment
- ✅ Comprehensive documentation

### What's Next (Future Enhancements)
- [ ] Integrate real ASL video dataset (e.g., WLASL)
- [ ] 3D avatar animation
- [ ] ML-based sign language generation
- [ ] Authentication and rate limiting
- [ ] Multiple sign languages (BSL, ISL, etc.)
- [ ] WebSocket streaming
- [ ] Comprehensive tests
- [ ] Performance benchmarks

## Technology Stack

- **Backend**: FastAPI, Python 3.11+
- **Video**: OpenCV, Pillow
- **LLM Integration**: OpenAI SDK, Anthropic SDK
- **Demo**: Streamlit
- **Deployment**: Docker, Docker Compose
- **CI/CD**: GitHub Actions
- **Registry**: GitHub Container Registry (GHCR)

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v1/chat/completions` | POST | OpenAI-compatible chat |
| `/v1/models` | GET | List available models |
| `/api/sign-language/generate` | POST | Direct text-to-sign |
| `/api/sign-language/video/{filename}` | GET | Video info |
| `/health` | GET | Health check |
| `/docs` | GET | Swagger UI |

## Links

- **GitHub**: https://github.com/NotYuSheng/GestureGPT
- **Docker Image**: ghcr.io/notyusheng/gesturegpt:latest
- **API Docs**: http://localhost:8000/docs (when running)
- **Demo**: http://localhost:8501 (when running)

## Support

- **Issues**: https://github.com/NotYuSheng/GestureGPT/issues
- **Discussions**: https://github.com/NotYuSheng/GestureGPT/discussions

## License

Educational and personal use.

---

**Built with ❤️ for the sign language community**
