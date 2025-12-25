# GestureGPT Demo

Interactive Streamlit demo for GestureGPT - a sign language LLM-style API.

## Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# From the demo directory
cd demo

# Start both backend and demo
docker-compose up -d

# Access the demo at http://localhost:8501
```

This will:
1. Pull the backend from GHCR
2. Build the Streamlit demo
3. Start both services

### Option 2: Backend Only (Without Demo UI)

```bash
cd demo

# Just run the backend
docker-compose up -d backend

# Access API docs at http://localhost:8000/docs
```

### Option 3: Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Make sure backend is running (see above or use existing instance)

# Run Streamlit
streamlit run streamlit_app.py

# Or specify backend URL
SIGNALAPI_URL=http://localhost:8000 streamlit run streamlit_app.py
```

## Configuration

### Environment Variables

Create a `.env` file in the demo directory:

```bash
# For backend LLM configuration (optional)
OPENAI_API_KEY=sk-...
LLM_PROVIDER=openai
OPENAI_MODEL=gpt-3.5-turbo

# For demo app
SIGNALAPI_URL=http://backend:8000
```

### Using Real LLM

Edit `docker-compose.yml` and uncomment the LLM configuration:

```yaml
environment:
  # LLM Configuration
  - LLM_PROVIDER=openai
  - OPENAI_API_KEY=${OPENAI_API_KEY}
  - OPENAI_MODEL=gpt-3.5-turbo
```

Then create `.env`:
```bash
OPENAI_API_KEY=sk-your-actual-key-here
```

See [LLM Configuration Guide](../docs/LLM_CONFIGURATION.md) for more options.

## Features

The demo provides three tabs:

### 💬 Chat
- Interactive chat interface
- Displays both text responses and sign language videos
- Conversation history
- Clear chat functionality

### 🎯 Direct Conversion
- Convert any text directly to sign language
- Choose video format (MP4 or GIF)
- Download generated videos
- View video metadata

### 📚 API Docs
- Example code snippets
- API endpoint documentation
- Model information

## Usage

### Chat Mode

1. Open http://localhost:8501
2. Go to the "Chat" tab
3. Type your message in the chat input
4. Receive text response + sign language video

### Direct Conversion Mode

1. Go to the "Direct Conversion" tab
2. Enter text in the text area
3. Choose video format (MP4 or GIF)
4. Click "Generate Sign Language Video"
5. View or download the result

## Screenshots

### Chat Interface
![Chat Interface](../docs/images/chat-demo.png) *(placeholder)*

### Direct Conversion
![Direct Conversion](../docs/images/direct-demo.png) *(placeholder)*

## Development

### File Structure

```
demo/
├── streamlit_app.py      # Main Streamlit app
├── requirements.txt      # Python dependencies
├── Dockerfile           # Demo container image
├── docker-compose.yml   # Orchestration (backend + demo)
└── README.md           # This file
```

### Customization

Edit `streamlit_app.py` to customize:
- UI theme and styling
- Chat prompts
- Example messages
- Video display settings

### Local Development Workflow

```bash
# Terminal 1: Run backend
cd ..
python -m app.main

# Terminal 2: Run demo with hot reload
cd demo
streamlit run streamlit_app.py
```

## Troubleshooting

### "API Offline" Error

Check if backend is running:
```bash
curl http://localhost:8000/health
```

If not running:
```bash
docker-compose up -d backend
```

### Can't Access Demo

Make sure port 8501 is not in use:
```bash
lsof -i :8501
```

Change port in docker-compose.yml if needed:
```yaml
ports:
  - "8502:8501"  # Use 8502 instead
```

### Video Not Displaying

1. Check browser console for errors
2. Verify video URL is accessible
3. Check backend logs: `docker-compose logs backend`

### Demo Crashes

Check logs:
```bash
docker-compose logs demo
```

Restart demo:
```bash
docker-compose restart demo
```

## Stopping the Demo

```bash
# Stop all services
docker-compose down

# Stop but keep containers
docker-compose stop

# Remove everything including volumes
docker-compose down -v
```

## Production Deployment

For production deployment of the demo:

1. **Add Authentication**
   ```python
   # Add to streamlit_app.py
   import streamlit_authenticator as stauth
   # Configure auth
   ```

2. **Use HTTPS**
   - Deploy behind reverse proxy (Nginx)
   - Add SSL certificates

3. **Resource Limits**
   ```yaml
   # In docker-compose.yml
   deploy:
     resources:
       limits:
         cpus: '1.0'
         memory: 512M
   ```

4. **Environment Variables**
   ```bash
   # Use secrets management
   docker secret create openai_key openai_key.txt
   ```

## Support

For issues with the demo:
1. Check [troubleshooting](#troubleshooting) above
2. View [backend docs](../docs/)
3. Open issue: https://github.com/NotYuSheng/GestureGPT/issues

## Links

- [Main README](../README.md)
- [API Documentation](http://localhost:8000/docs)
- [LLM Configuration](../docs/LLM_CONFIGURATION.md)
- [Deployment Guide](../docs/DEPLOYMENT.md)
