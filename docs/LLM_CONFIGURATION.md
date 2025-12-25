# LLM Configuration Guide

GestureGPT supports multiple LLM providers for generating text responses that are then converted to sign language videos. This guide explains how to configure different LLM backends.

## Overview

The text generation flow is:
1. User sends a message
2. **LLM generates a text response** (configured here)
3. Text response is converted to sign language video
4. Returns video URL + text

## Supported Providers

- **placeholder** - Simple canned responses (default, no API key needed)
- **openai** - OpenAI GPT models (gpt-3.5-turbo, gpt-4, etc.)
- **anthropic** - Anthropic Claude models
- **custom** - Any OpenAI-compatible endpoint (Ollama, LM Studio, etc.)

## Configuration via Environment Variables

All LLM configuration is done through the `.env` file. Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
# Edit .env with your preferred provider
```

## Provider Setup

### 1. Placeholder (Default)

No setup required. Uses simple keyword-based responses.

```bash
LLM_PROVIDER=placeholder
```

Good for:
- Testing the API
- Development
- Demo purposes

### 2. OpenAI

**Requirements:**
- OpenAI API key
- Install package: `pip install openai`

**Configuration:**

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...your-key-here...
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_BASE_URL=https://api.openai.com/v1  # Optional
```

**Available Models:**
- `gpt-3.5-turbo` - Fast and cost-effective
- `gpt-4` - More capable but slower/expensive
- `gpt-4-turbo` - Latest GPT-4 with better performance

**Get API Key:** https://platform.openai.com/api-keys

### 3. Anthropic Claude

**Requirements:**
- Anthropic API key
- Install package: `pip install anthropic`

**Configuration:**

```bash
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...your-key-here...
ANTHROPIC_MODEL=claude-3-opus-20240229
```

**Available Models:**
- `claude-3-haiku-20240307` - Fast and economical
- `claude-3-sonnet-20240229` - Balanced performance
- `claude-3-opus-20240229` - Most capable

**Get API Key:** https://console.anthropic.com/

### 4. Custom / Local LLM

Use any OpenAI-compatible endpoint like Ollama, LM Studio, LocalAI, etc.

**Requirements:**
- Install package: `pip install openai`
- Running LLM server

**Configuration:**

```bash
LLM_PROVIDER=custom
CUSTOM_LLM_ENDPOINT=http://localhost:11434/v1/chat/completions
CUSTOM_LLM_MODEL=llama2
CUSTOM_LLM_API_KEY=optional_api_key  # Often not needed for local
```

#### Example: Using Ollama

```bash
# Install Ollama: https://ollama.ai
# Pull a model
ollama pull llama2

# Ollama runs on port 11434 by default
# Configure .env:
LLM_PROVIDER=custom
CUSTOM_LLM_ENDPOINT=http://localhost:11434/v1/chat/completions
CUSTOM_LLM_MODEL=llama2
CUSTOM_LLM_API_KEY=not-needed
```

#### Example: Using LM Studio

**Step-by-Step LM Studio Setup:**

1. **Download and Install LM Studio**
   - Visit https://lmstudio.ai/
   - Download for your platform (Windows/Mac/Linux)
   - Install and launch LM Studio

2. **Download a Model**
   - Open LM Studio
   - Click on the 🔍 Search tab
   - Search for a model (recommended: `TheBloke/Llama-2-7B-Chat-GGUF`)
   - Click Download on your preferred model
   - Wait for download to complete

3. **Load the Model**
   - Go to the 💬 Chat tab
   - Click "Select a model to load"
   - Choose your downloaded model
   - Click "Load Model"
   - Wait for model to load (you'll see "Model loaded" message)

4. **Start the Local Server**
   - Click on the ⚡ "Local Server" tab (left sidebar)
   - Click "Start Server"
   - Server will start on `http://localhost:1234` (default port)
   - You should see "Server running on port 1234"

5. **Configure GestureGPT**

   Edit your `.env` file:
   ```bash
   LLM_PROVIDER=custom
   CUSTOM_LLM_ENDPOINT=http://localhost:1234/v1/chat/completions
   CUSTOM_LLM_MODEL=local-model  # Can be any name
   CUSTOM_LLM_API_KEY=not-needed
   ```

6. **Test the Connection**
   ```bash
   # Test LM Studio server is running
   curl http://localhost:1234/v1/models

   # Start GestureGPT
   cd demo
   docker-compose up -d

   # Check logs to confirm LLM connected
   docker-compose logs backend | grep "Custom LLM"
   # Should see: "✓ Custom LLM provider initialized: http://localhost:1234/v1/chat/completions"
   ```

7. **Using with Docker**

   If running GestureGPT in Docker, use `host.docker.internal` instead of `localhost`:

   ```bash
   # In .env or docker-compose.yml
   LLM_PROVIDER=custom
   CUSTOM_LLM_ENDPOINT=http://host.docker.internal:1234/v1/chat/completions
   CUSTOM_LLM_MODEL=local-model
   ```

   Or on Linux, use host network mode:
   ```yaml
   # In docker-compose.yml
   services:
     backend:
       network_mode: "host"
       # ... rest of config
   ```

**Recommended Models for LM Studio:**

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| **Llama-2-7B-Chat** | 7B | Fast | Good | General chat, quick responses |
| **Mistral-7B-Instruct** | 7B | Fast | Excellent | Instruction following |
| **Llama-2-13B-Chat** | 13B | Medium | Very Good | Better reasoning |
| **OpenHermes-2.5-Mistral** | 7B | Fast | Excellent | Conversational |
| **Phi-2** | 2.7B | Very Fast | Good | Resource-constrained systems |

**Tips:**
- Start with a 7B model for best balance of speed/quality
- Use GGUF format models (optimized for CPU)
- Quantized models (Q4, Q5) are smaller and faster
- Adjust context length in LM Studio settings if needed

## Docker Configuration

### Using Docker Compose

Add environment variables to `docker-compose.yml`:

```yaml
services:
  backend:
    image: ghcr.io/notyusheng/gesturegpt:latest
    environment:
      # LLM Configuration
      - LLM_PROVIDER=openai
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENAI_MODEL=gpt-3.5-turbo
```

Then create a `.env` file in the same directory:

```bash
OPENAI_API_KEY=sk-...your-key...
```

### Using Docker Run

Pass environment variables directly:

```bash
docker run -d \
  -p 8000:8000 \
  -e LLM_PROVIDER=openai \
  -e OPENAI_API_KEY=sk-...your-key... \
  -e OPENAI_MODEL=gpt-3.5-turbo \
  ghcr.io/notyusheng/gesturegpt:latest
```

## Verification

After configuring, check the startup logs:

```bash
# Docker Compose
docker-compose logs backend

# Docker
docker logs gesturegpt-backend

# Local
python -m app.main
```

You should see one of:
- `✓ OpenAI provider initialized with model: gpt-3.5-turbo`
- `✓ Anthropic provider initialized with model: claude-3-opus-20240229`
- `✓ Custom LLM provider initialized: http://localhost:11434/v1/chat/completions`
- `ℹ Using placeholder LLM provider (canned responses)`

## Testing

Test your LLM configuration:

```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gesturegpt-v1",
    "messages": [
      {"role": "user", "content": "Tell me a short joke about sign language"}
    ]
  }'
```

You should get:
- A relevant text response from your LLM
- A video URL with the sign language version

## Troubleshooting

### "OpenAI package not installed"

```bash
pip install openai
# or
pip install anthropic
```

Then rebuild Docker image if using Docker.

### "API key not valid"

Check your API key:
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/

Make sure it's properly set in `.env`:
```bash
OPENAI_API_KEY=sk-proj-...  # Should start with sk-
```

### "Connection refused" (Custom endpoint)

Make sure your local LLM server is running:

```bash
# For Ollama
ollama serve

# Check if accessible
curl http://localhost:11434/v1/models
```

### Falling back to placeholder

If initialization fails, the system automatically falls back to placeholder mode. Check logs for warnings:

```bash
⚠ OpenAI initialization failed: Invalid API key
ℹ Using placeholder LLM provider (canned responses)
```

## Cost Optimization

### OpenAI

- Use `gpt-3.5-turbo` for most cases (cheaper)
- Set `max_tokens` in `.env` to limit response length (future feature)
- Monitor usage: https://platform.openai.com/usage

### Anthropic

- Use `claude-3-haiku` for simple responses (most economical)
- Use `claude-3-sonnet` for better quality
- Reserve `claude-3-opus` for complex interactions

### Free Options

1. **Ollama** (100% free, runs locally)
   ```bash
   ollama pull llama2
   # Use with CUSTOM provider
   ```

2. **LM Studio** (100% free, runs locally)
   - Download from https://lmstudio.ai
   - Load any Hugging Face model
   - Start server and use with CUSTOM provider

## Best Practices

1. **Security**
   - Never commit `.env` file with API keys
   - Use environment variables in production
   - Rotate API keys regularly

2. **Performance**
   - Use faster models (gpt-3.5-turbo, claude-haiku) for better response times
   - Local LLMs eliminate API latency but require more resources

3. **Reliability**
   - Placeholder mode always works as fallback
   - System auto-falls-back if LLM fails
   - Consider rate limiting for production

## Advanced Configuration

### Multiple Models

To support different models, you can modify the LLM service to accept model parameter from requests. However, the current design uses environment-based configuration for:
- Better security (API keys not in requests)
- Simpler deployment
- Consistent behavior

### Custom System Prompts

Edit [app/services/llm_service.py](../app/services/llm_service.py) to add system prompts:

```python
def generate_response(self, messages: List[ChatMessage]) -> str:
    # Add system prompt
    system_msg = ChatMessage(
        role="system",
        content="You are a helpful sign language assistant. Keep responses brief and clear."
    )
    messages = [system_msg] + messages
    # ... continue with generation
```

## Example Configurations

### Development

```bash
LLM_PROVIDER=placeholder
```

### Production (Cloud)

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=${OPENAI_API_KEY}  # From secrets
OPENAI_MODEL=gpt-3.5-turbo
```

### Self-Hosted

```bash
LLM_PROVIDER=custom
CUSTOM_LLM_ENDPOINT=http://llm-server:11434/v1/chat/completions
CUSTOM_LLM_MODEL=llama2
```

## Support

For issues with LLM configuration:
1. Check the logs for initialization messages
2. Verify API keys are correct
3. Test API connectivity manually
4. Open an issue: https://github.com/NotYuSheng/GestureGPT/issues
