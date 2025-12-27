# GestureGPT Streamlit Demo

A simple chatbot interface to test the GestureGPT API.

## Quick Start

### Prerequisites

Make sure GestureGPT backend is running:

```bash
# From the project root
docker compose up -d

# Or run locally
python -m app.main
```

### Running the Demo

1. Create a virtual environment and install dependencies:

```bash
cd demo
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

2. Run the Streamlit app:

```bash
venv/bin/streamlit run streamlit_app.py
```

3. Open your browser to http://localhost:8501

## Configuration

The demo connects to GestureGPT at `http://localhost:8000` by default. You can override this by setting the `GESTUREGPT_URL` environment variable:

```bash
GESTUREGPT_URL=http://your-api:8000 venv/bin/streamlit run streamlit_app.py
```

## Features

The demo provides three tabs:

### 💬 Chat
- Interactive chat interface
- Displays multiple sign language videos per response (one per word)
- Shows warnings for missing videos
- Conversation history
- Clear chat functionality

### 🎯 Direct Conversion
- Convert any text directly to sign language
- View original and normalized text
- Displays array of video URLs
- Shows which words have missing videos
- Choose video format (MP4 or GIF)

### 📚 API Docs
- Example code snippets for both endpoints
- OpenAI SDK usage examples
- Model information

## Usage

### Chat Mode

1. Open http://localhost:8501
2. Go to the "Chat" tab
3. Type your message in the chat input
4. The LLM generates an ASL-friendly response
5. Each word's video is displayed in sequence
6. Missing videos are highlighted with warnings

### Direct Conversion Mode

1. Go to the "Direct Conversion" tab
2. Enter text in the text area (max 500 characters)
3. Choose video format (MP4 or GIF)
4. Click "Generate Sign Language Video"
5. View the normalized text and all video URLs
6. See which words are missing videos

## Troubleshooting

### "API Offline" Error

Check if backend is running:
```bash
curl http://localhost:8000/health
```

If not running:
```bash
docker compose up -d
```

### Port 8501 Already in Use

Kill existing Streamlit processes:
```bash
lsof -ti:8501 | xargs kill -9
```

Or use a different port:
```bash
venv/bin/streamlit run streamlit_app.py --server.port 8502
```

### Videos Not Displaying

1. Check that the backend is accessible
2. Verify video URLs in the browser console
3. Check backend logs for errors

## Development

### File Structure

```
demo/
├── streamlit_app.py      # Main Streamlit app
├── requirements.txt      # Python dependencies
├── venv/                # Virtual environment (gitignored)
└── README.md           # This file
```

### Local Development Workflow

```bash
# Terminal 1: Run backend
cd /home/ubuntu/Desktop/GestureGPT
docker compose up -d

# Terminal 2: Run demo with hot reload
cd demo
venv/bin/streamlit run streamlit_app.py
```
