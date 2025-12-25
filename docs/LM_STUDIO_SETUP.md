# LM Studio Setup Guide for GestureGPT

Complete guide to setting up LM Studio as a local LLM backend for GestureGPT.

## What is LM Studio?

LM Studio is a desktop application that lets you run Large Language Models (LLMs) locally on your computer. It provides:
- Easy model download and management
- OpenAI-compatible local API server
- No API costs or internet dependency
- Privacy - everything runs locally

## Prerequisites

- **RAM**: 8GB minimum (16GB+ recommended)
- **Storage**: 5-20GB for models
- **OS**: Windows 10/11, macOS 11+, or Linux
- **Internet**: Only for initial model download

## Step-by-Step Setup

### 1. Install LM Studio

1. Visit https://lmstudio.ai/
2. Click "Download LM Studio"
3. Choose your platform:
   - Windows: Download `.exe` installer
   - macOS: Download `.dmg` file
   - Linux: Download AppImage
4. Install and launch LM Studio

### 2. Download a Model

#### For Beginners (Recommended)

1. Open LM Studio
2. Click the **🔍 Search** icon (left sidebar)
3. In the search box, type: `mistral-7b-instruct`
4. Find **"TheBloke/Mistral-7B-Instruct-v0.2-GGUF"**
5. Click the model card
6. Choose a quantization:
   - **Q4_K_M** - Best balance (4GB RAM)
   - **Q5_K_M** - Better quality (5GB RAM)
   - **Q8_0** - Highest quality (8GB RAM)
7. Click **Download**
8. Wait for download to complete (progress bar shown)

#### Model Recommendations by System

**8GB RAM:**
```
Model: TheBloke/Phi-2-GGUF
Quantization: Q4_K_M
Size: ~1.6GB
```

**16GB RAM:**
```
Model: TheBloke/Mistral-7B-Instruct-v0.2-GGUF
Quantization: Q5_K_M
Size: ~5GB
```

**32GB+ RAM:**
```
Model: TheBloke/Llama-2-13B-Chat-GGUF
Quantization: Q5_K_M
Size: ~9GB
```

### 3. Load the Model

1. Click the **💬 Chat** tab (left sidebar)
2. At the top, click **"Select a model to load"**
3. Choose your downloaded model from the list
4. Click **"Load Model"**
5. Wait for the model to load (status shown at top)
6. You should see "✅ Model loaded successfully"

**Optional:** Test the model in the chat interface to make sure it works.

### 4. Start the Local Server

1. Click the **⚙️ Developer** tab (or **⚡ Local Server**)
2. Review server settings:
   - **Port**: 1234 (default, or change if needed)
   - **CORS**: Enable if accessing from browser
   - **API Key**: Leave empty (not needed for local use)
3. Click **"Start Server"**
4. You should see: **"Server running on port 1234"**
5. The endpoint will be: `http://localhost:1234`

### 5. Test the Server

Open a terminal and test:

```bash
# Test if server is running
curl http://localhost:1234/v1/models

# Should return JSON with model info
```

Or test a chat completion:

```bash
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Hello!"}],
    "temperature": 0.7
  }'
```

### 6. Configure GestureGPT

#### Option A: Local Installation

Edit `.env` in your GestureGPT directory:

```bash
# LLM Configuration
LLM_PROVIDER=custom
CUSTOM_LLM_ENDPOINT=http://localhost:1234/v1/chat/completions
CUSTOM_LLM_MODEL=local-model
CUSTOM_LLM_API_KEY=not-needed
```

Then start GestureGPT:

```bash
python -m app.main
```

#### Option B: Docker (Same Machine)

If running GestureGPT in Docker on the **same machine**:

**On Windows/Mac:**
```yaml
# demo/docker-compose.yml
services:
  backend:
    environment:
      - LLM_PROVIDER=custom
      - CUSTOM_LLM_ENDPOINT=http://host.docker.internal:1234/v1/chat/completions
      - CUSTOM_LLM_MODEL=local-model
```

**On Linux:**
```yaml
# demo/docker-compose.yml
services:
  backend:
    network_mode: "host"
    environment:
      - LLM_PROVIDER=custom
      - CUSTOM_LLM_ENDPOINT=http://localhost:1234/v1/chat/completions
      - CUSTOM_LLM_MODEL=local-model
```

Or create a `.env` file in the `demo/` directory:

```bash
# demo/.env
LLM_PROVIDER=custom
CUSTOM_LLM_ENDPOINT=http://host.docker.internal:1234/v1/chat/completions
CUSTOM_LLM_MODEL=local-model
CUSTOM_LLM_API_KEY=not-needed
```

Then update `docker-compose.yml`:

```yaml
services:
  backend:
    env_file:
      - .env
```

### 7. Start GestureGPT and Test

```bash
cd demo
docker-compose up -d

# Check logs
docker-compose logs backend

# You should see:
# ✓ Custom LLM provider initialized: http://host.docker.internal:1234/v1/chat/completions
```

Test the integration:

```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gesturegpt-v1",
    "messages": [{"role": "user", "content": "Tell me a short joke"}]
  }'
```

You should get a response with both text and a video URL!

## Complete Demo Setup

Here's a complete workflow to run the full GestureGPT demo with LM Studio:

```bash
# 1. Start LM Studio (GUI)
#    - Load your model
#    - Start local server on port 1234

# 2. Configure GestureGPT
cd GestureGPT/demo
cat > .env << 'EOF'
LLM_PROVIDER=custom
CUSTOM_LLM_ENDPOINT=http://host.docker.internal:1234/v1/chat/completions
CUSTOM_LLM_MODEL=local-model
EOF

# 3. Start backend and demo
docker-compose up -d

# 4. Open browser
# Backend API: http://localhost:8000/docs
# Demo UI: http://localhost:8501

# 5. Test in demo
# Go to http://localhost:8501
# Send a message in chat - it will use your local LLM!
```

## Troubleshooting

### "Connection refused" Error

**Problem**: GestureGPT can't connect to LM Studio

**Solutions**:
1. Make sure LM Studio server is running (check Developer tab)
2. Verify port is correct (default: 1234)
3. On Windows/Mac Docker: Use `host.docker.internal` instead of `localhost`
4. On Linux Docker: Use `network_mode: "host"` or actual IP address
5. Test connectivity:
   ```bash
   # From your host
   curl http://localhost:1234/v1/models

   # From inside Docker container
   docker exec gesturegpt-backend curl http://host.docker.internal:1234/v1/models
   ```

### Model Not Loading

**Problem**: LM Studio shows error when loading model

**Solutions**:
1. Check you have enough RAM (model size + 2GB overhead)
2. Close other applications
3. Try a smaller model or lower quantization
4. Restart LM Studio

### Slow Responses

**Problem**: LLM takes too long to respond

**Solutions**:
1. Use a smaller model (7B instead of 13B)
2. Use lower quantization (Q4 instead of Q8)
3. Reduce context length in LM Studio settings
4. Close other applications
5. Enable GPU acceleration if available (LM Studio Settings)

### LM Studio Server Stops

**Problem**: Server stops after some time

**Solutions**:
1. Check LM Studio hasn't crashed (restart if needed)
2. Disable sleep/hibernate on your computer
3. Check firewall isn't blocking port 1234
4. Review LM Studio logs for errors

### Docker Can't Reach LM Studio

**Problem**: Works locally but not from Docker

**Solutions**:

**Windows/Mac:**
```bash
# Use host.docker.internal
CUSTOM_LLM_ENDPOINT=http://host.docker.internal:1234/v1/chat/completions
```

**Linux:**
```bash
# Option 1: Use host network
docker run --network host ...

# Option 2: Use host IP
# Find your IP: ip addr show | grep inet
CUSTOM_LLM_ENDPOINT=http://192.168.1.100:1234/v1/chat/completions
```

## Advanced Configuration

### Custom System Prompt

Edit LM Studio's system prompt for sign language context:

1. In LM Studio, go to Developer tab
2. Find "System Prompt" section
3. Add:
   ```
   You are a helpful assistant for a sign language translation system.
   Provide clear, concise responses that work well when converted to sign language.
   Use simple vocabulary and short sentences.
   ```

### Performance Tuning

In LM Studio Settings:

- **Context Length**: Lower for faster responses (1024-2048)
- **Batch Size**: Increase if you have RAM (512-1024)
- **Threads**: Set to CPU core count - 2
- **GPU Layers**: Max out if you have a GPU

### Running Multiple Models

You can run LM Studio on different ports for different purposes:

1. Port 1234: Fast model (Phi-2) for quick responses
2. Port 1235: Quality model (Mistral-7B) for important queries

Configure which port to use in `.env`.

## Best Practices

1. **Keep LM Studio Running**: Start it when you boot your computer
2. **Monitor Resources**: Watch RAM/CPU usage in Task Manager
3. **Regular Updates**: Update LM Studio when new versions release
4. **Model Management**: Delete unused models to save space
5. **Backup Configs**: Save your `.env` settings

## Model Recommendations

### For Demo/Testing

```
Model: TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF
Quantization: Q4_K_M
Pros: Very fast, low resource usage
Cons: Lower quality responses
```

### For Production

```
Model: TheBloke/Mistral-7B-Instruct-v0.2-GGUF
Quantization: Q5_K_M
Pros: Great balance of speed and quality
Cons: Requires 16GB RAM
```

### For Best Quality

```
Model: TheBloke/Llama-2-13B-Chat-GGUF
Quantization: Q5_K_M
Pros: Excellent responses
Cons: Slower, requires 32GB RAM
```

## Alternative: Ollama

If you prefer command-line:

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull mistral

# Start server (runs on port 11434)
ollama serve

# Configure GestureGPT
LLM_PROVIDER=custom
CUSTOM_LLM_ENDPOINT=http://localhost:11434/v1/chat/completions
CUSTOM_LLM_MODEL=mistral
```

## Support

For issues:
- LM Studio: https://lmstudio.ai/docs
- GestureGPT: https://github.com/NotYuSheng/GestureGPT/issues

## Next Steps

Once LM Studio is working:
1. Try different models to find your favorite
2. Experiment with system prompts
3. Integrate with your applications
4. Share your setup with others!

---

**Happy local LLM testing!** 🚀
