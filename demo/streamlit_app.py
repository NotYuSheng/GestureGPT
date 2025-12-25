import streamlit as st
import requests
import os
from datetime import datetime

# Configuration
SIGNALAPI_URL = os.getenv("SIGNALAPI_URL", "http://localhost:8000")

# Page config
st.set_page_config(
    page_title="SignalAPI Demo",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 3rem;
    }
    .video-container {
        display: flex;
        justify-content: center;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">👋 SignalAPI Demo</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-powered Sign Language Generation</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")

    api_mode = st.radio(
        "API Mode",
        ["Chat (OpenAI-compatible)", "Direct Conversion"],
        help="Choose between chat-based or direct text-to-sign conversion"
    )

    video_format = st.selectbox(
        "Video Format",
        ["mp4", "gif"],
        help="Select output video format"
    )

    st.divider()

    st.header("ℹ️ About")
    st.info(
        "SignalAPI converts text to American Sign Language (ASL) videos. "
        "It features an OpenAI-compatible API for seamless integration."
    )

    # API Health Check
    try:
        health_response = requests.get(f"{SIGNALAPI_URL}/health", timeout=5)
        if health_response.status_code == 200:
            st.success("✅ API Connected")
            health_data = health_response.json()
            st.caption(f"Version: {health_data.get('version', 'Unknown')}")
        else:
            st.error("❌ API Error")
    except:
        st.error("❌ API Offline")
        st.caption(f"Endpoint: {SIGNALAPI_URL}")

# Main content
tab1, tab2, tab3 = st.tabs(["💬 Chat", "🎯 Direct Conversion", "📚 API Docs"])

with tab1:
    st.header("Chat with SignalAPI")
    st.markdown("Send messages and receive responses in sign language!")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "video_url" in message:
                st.video(message["video_url"])

    # Chat input
    if prompt := st.chat_input("Type your message..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get response from API
        with st.chat_message("assistant"):
            with st.spinner("Generating sign language response..."):
                try:
                    # Prepare messages for API
                    api_messages = [
                        {"role": msg["role"], "content": msg["content"]}
                        for msg in st.session_state.messages
                    ]

                    response = requests.post(
                        f"{SIGNALAPI_URL}/v1/chat/completions",
                        json={
                            "model": "signalapi-v1",
                            "messages": api_messages,
                            "format": video_format
                        },
                        timeout=30
                    )

                    if response.status_code == 200:
                        data = response.json()
                        assistant_message = data["choices"][0]["message"]["content"]
                        video_url = data["choices"][0].get("video_url", "")

                        st.markdown(assistant_message)
                        if video_url:
                            st.video(video_url)

                        # Add assistant message to chat
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": assistant_message,
                            "video_url": video_url
                        })
                    else:
                        st.error(f"API Error: {response.status_code}")
                        st.json(response.json())

                except Exception as e:
                    st.error(f"Error: {str(e)}")

    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

with tab2:
    st.header("Direct Text to Sign Language")
    st.markdown("Convert any text directly to sign language video")

    col1, col2 = st.columns([2, 1])

    with col1:
        text_input = st.text_area(
            "Enter text to convert:",
            placeholder="Type something like 'Hello, how are you?' or 'Good morning!'",
            height=150,
            max_chars=500
        )

        include_subtitles = st.checkbox("Include text subtitles", value=True)

        generate_button = st.button("🎬 Generate Sign Language Video", type="primary", use_container_width=True)

    with col2:
        st.info(
            "**Tips:**\n"
            "- Keep text concise\n"
            "- Use clear sentences\n"
            "- Max 500 characters\n"
            f"- Format: {video_format.upper()}"
        )

    if generate_button and text_input:
        with st.spinner("Generating sign language video..."):
            try:
                response = requests.post(
                    f"{SIGNALAPI_URL}/api/sign-language/generate",
                    json={
                        "text": text_input,
                        "format": video_format,
                        "include_subtitles": include_subtitles
                    },
                    timeout=30
                )

                if response.status_code == 200:
                    data = response.json()

                    st.success("✅ Video generated successfully!")

                    # Display video
                    st.markdown("### Generated Video")
                    st.video(data["video_url"])

                    # Display metadata
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Duration", f"{data.get('duration', 0):.1f}s")
                    with col2:
                        st.metric("Format", data.get('format', 'N/A').upper())
                    with col3:
                        st.metric("Status", "✅ Success" if data.get('success') else "❌ Failed")

                    # Show text
                    if data.get('text'):
                        st.markdown("### Original Text")
                        st.info(data['text'])

                    # Download button
                    st.markdown("### Download")
                    st.markdown(f"[📥 Download Video]({data['video_url']})")

                else:
                    st.error(f"API Error: {response.status_code}")
                    st.json(response.json())

            except Exception as e:
                st.error(f"Error: {str(e)}")

    elif generate_button and not text_input:
        st.warning("⚠️ Please enter some text first!")

with tab3:
    st.header("API Documentation")

    st.markdown("""
    ### OpenAI-Compatible Chat Endpoint

    **POST** `/v1/chat/completions`

    ```python
    import requests

    response = requests.post(
        "http://localhost:8000/v1/chat/completions",
        json={
            "model": "signalapi-v1",
            "messages": [
                {"role": "user", "content": "Hello, how are you?"}
            ],
            "format": "mp4"
        }
    )
    ```

    ### Direct Sign Language Endpoint

    **POST** `/api/sign-language/generate`

    ```python
    response = requests.post(
        "http://localhost:8000/api/sign-language/generate",
        json={
            "text": "Hello, how are you?",
            "format": "mp4",
            "include_subtitles": true
        }
    )
    ```

    ### Using with OpenAI Python SDK

    ```python
    from openai import OpenAI

    client = OpenAI(
        base_url="http://localhost:8000/v1",
        api_key="not-needed"
    )

    response = client.chat.completions.create(
        model="signalapi-v1",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    ```
    """)

    st.divider()

    st.markdown("### Available Models")
    try:
        models_response = requests.get(f"{SIGNALAPI_URL}/v1/models", timeout=5)
        if models_response.status_code == 200:
            st.json(models_response.json())
        else:
            st.error("Failed to fetch models")
    except:
        st.error("API unavailable")

# Footer
st.divider()
st.markdown(
    """
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p>SignalAPI - Sign Language LLM-style API</p>
        <p>Built with FastAPI, Streamlit, and OpenCV</p>
    </div>
    """,
    unsafe_allow_html=True
)
