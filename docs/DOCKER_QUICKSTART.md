# Docker Quick Start Guide

Get GestureGPT running in under 2 minutes!

## Prerequisites

- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (included with Docker Desktop)

## Option 1: Using Pre-built Image (Recommended)

```bash
# Clone the repository
git clone https://github.com/NotYuSheng/GestureGPT.git
cd GestureGPT

# Start the backend API
docker-compose up -d

# Wait a few seconds for startup, then test
curl http://localhost:8000/health
```

That's it! The API is now running at `http://localhost:8000`

## Option 2: With Streamlit Demo

```bash
# Start both backend and demo
docker-compose --profile demo up -d

# Open your browser to:
# - API: http://localhost:8000/docs
# - Demo: http://localhost:8501
```

## Quick Test

### Test the API with curl

```bash
# Test chat endpoint (OpenAI-compatible)
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gesturegpt-v1",
    "messages": [{"role": "user", "content": "Hello!"}],
    "format": "mp4"
  }'

# Test direct conversion
curl -X POST "http://localhost:8000/api/sign-language/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, how are you?",
    "format": "mp4"
  }'
```

### Test with Python

```bash
# Install requests
pip install requests

# Run test
python -c "
import requests
response = requests.post(
    'http://localhost:8000/v1/chat/completions',
    json={
        'model': 'gesturegpt-v1',
        'messages': [{'role': 'user', 'content': 'Hello!'}]
    }
)
print(response.json())
"
```

## View API Documentation

Open in your browser:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Common Commands

```bash
# View logs
docker-compose logs -f backend

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Update to latest image
docker-compose pull
docker-compose up -d

# View running containers
docker ps

# Check container health
docker ps --filter "name=gesturegpt-backend"
```

## Troubleshooting

### Port Already in Use

If port 8000 is already in use, edit `docker-compose.yml`:

```yaml
ports:
  - "8080:8000"  # Change 8000 to 8080 or another port
```

### Can't Pull Image

If you get permission errors:

```bash
# Make sure you're logged in to GitHub
docker login ghcr.io -u YOUR_GITHUB_USERNAME
```

Or build locally:

```bash
# Build the image yourself
docker build -t gesturegpt:local .

# Edit docker-compose.yml and change:
# image: ghcr.io/notyusheng/gesturegpt:latest
# to:
# image: gesturegpt:local
```

### Container Won't Start

```bash
# Check logs
docker-compose logs backend

# Remove and recreate
docker-compose down
docker-compose up -d
```

## Next Steps

- Read the full [API Documentation](README.md)
- Check out [Deployment Guide](DEPLOYMENT.md) for production setup
- Try the [Streamlit Demo](demo/streamlit_app.py)

## Stopping the Services

```bash
# Stop containers (keeps data)
docker-compose stop

# Stop and remove containers (keeps volumes)
docker-compose down

# Stop and remove everything including volumes
docker-compose down -v
```
