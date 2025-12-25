# GestureGPT Documentation

Welcome to the GestureGPT documentation!

## Quick Links

- [Docker Quick Start](DOCKER_QUICKSTART.md) - Get running in 2 minutes
- [LLM Configuration](LLM_CONFIGURATION.md) - Configure text generation backend
- [Deployment Guide](DEPLOYMENT.md) - Production deployment instructions

## Documentation Index

### Getting Started

1. **[Docker Quick Start](DOCKER_QUICKSTART.md)**
   - Prerequisites
   - Quick installation
   - Testing the API
   - Common commands
   - Troubleshooting

### Configuration

2. **[LLM Configuration](LLM_CONFIGURATION.md)**
   - Supported LLM providers
   - OpenAI setup
   - Anthropic Claude setup
   - Local LLM setup (Ollama, LM Studio)
   - Environment variables
   - Docker configuration

### Deployment

3. **[Deployment Guide](DEPLOYMENT.md)**
   - Docker Compose
   - Manual Docker commands
   - GHCR image usage
   - Production deployment
   - Kubernetes deployment
   - Reverse proxy setup
   - Monitoring and logs

## API Documentation

When the server is running, access interactive documentation at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Architecture

```
┌─────────────┐
│    User     │
└──────┬──────┘
       │ HTTP Request (text)
       ▼
┌─────────────────────────┐
│   GestureGPT API        │
│   (FastAPI)             │
└──────┬─────────┬────────┘
       │         │
       ▼         ▼
┌────────────┐  ┌──────────────┐
│ LLM Service│  │ Sign Service │
│ (OpenAI/   │  │ (Video Gen)  │
│  Claude/   │  │              │
│  Local)    │  │              │
└─────┬──────┘  └──────┬───────┘
      │                │
      │ Text Response  │
      └────────►───────┘
                │
                ▼
         ┌──────────────┐
         │ MP4/GIF Video│
         └──────────────┘
```

## Key Features

- **OpenAI-Compatible API**: Drop-in replacement for OpenAI endpoints
- **Multiple LLM Backends**: OpenAI, Claude, or local models
- **Video Generation**: Automatic ASL video creation
- **Docker Ready**: Pre-built images on GHCR
- **Streamlit Demo**: Interactive web interface

## Common Use Cases

### 1. Testing with Placeholder LLM

```bash
# No API key needed
LLM_PROVIDER=placeholder
docker-compose up -d
```

### 2. Production with OpenAI

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
docker-compose up -d
```

### 3. Self-Hosted with Local LLM

```bash
# Start Ollama
ollama serve
ollama pull llama2

# Configure GestureGPT
LLM_PROVIDER=custom
CUSTOM_LLM_ENDPOINT=http://localhost:11434/v1/chat/completions
docker-compose up -d
```

## Project Structure

```
GestureGPT/
├── app/
│   ├── api/              # API endpoints
│   ├── models/           # Pydantic schemas
│   ├── services/         # Business logic
│   └── main.py          # FastAPI app
├── demo/
│   └── streamlit_app.py # Web demo
├── docs/                # Documentation
├── output/              # Generated videos
├── .github/
│   └── workflows/       # CI/CD
├── Dockerfile           # Backend image
├── Dockerfile.demo      # Demo image
├── docker-compose.yml   # Orchestration
└── README.md           # Main readme
```

## Contributing

See the main [README](../README.md#contributing) for contribution guidelines.

## Support

- **Issues**: https://github.com/NotYuSheng/GestureGPT/issues
- **Discussions**: https://github.com/NotYuSheng/GestureGPT/discussions

## License

Educational and personal use. See main [README](../README.md) for details.
