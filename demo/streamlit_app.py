import os
import streamlit as st
import requests

# Configuration
GESTUREGPT_URL = os.getenv("GESTUREGPT_URL", "http://localhost:8000")

# Helper function to render video with autoplay
def render_video(video_url: str, autoplay: bool = True, max_size: str = "400px"):
    """Render a video with optional autoplay and custom size."""
    autoplay_attr = "autoplay muted loop" if autoplay else ""
    html = f"""
    <div class="video-container">
        <video {autoplay_attr} controls style="max-width: {max_size}; max-height: {max_size};">
            <source src="{video_url}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# Page config
st.set_page_config(
    page_title="GestureGPT Demo",
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
        margin: 1rem 0;
    }
    video {
        max-width: 400px;
        max-height: 400px;
        width: auto;
        height: auto;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">👋 GestureGPT Demo</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-powered Sign Language Generation</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")

    # Clear chat button at the top
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        if "messages" in st.session_state:
            st.session_state.messages = []
            st.rerun()

    st.divider()

    page_mode = st.radio(
        "Page Mode",
        ["💬 Chat", "🎯 Direct Conversion", "📚 API Docs"],
        help="Choose the interface mode"
    )

    video_format = st.selectbox(
        "Video Format",
        ["mp4", "gif"],
        help="Select output video format"
    )

    st.subheader("Video Playback")

    video_size = st.select_slider(
        "Video Size",
        options=["Small (200px)", "Medium (400px)", "Large (600px)", "X-Large (800px)"],
        value="Medium (400px)",
        help="Control the maximum size of sign language videos"
    )

    autoplay = st.checkbox(
        "Auto-play videos",
        value=True,
        help="Videos will play automatically when displayed"
    )

    st.divider()

    st.header("ℹ️ About")
    st.info(
        "GestureGPT converts text to American Sign Language (ASL) videos. "
        "It features an OpenAI-compatible API powered by vLLM for seamless integration."
    )

    # API Health Check
    try:
        health_response = requests.get(f"{GESTUREGPT_URL}/health", timeout=5)
        if health_response.status_code == 200:
            st.success("✅ API Connected")
            health_data = health_response.json()
            st.caption(f"Status: {health_data.get('status', 'Unknown')}")
        else:
            st.error("❌ API Error")
    except:
        st.error("❌ API Offline")
        st.caption(f"Endpoint: {GESTUREGPT_URL}")

# Extract pixel value from size setting
size_px = video_size.split("(")[1].split(")")[0]

# Main content - conditional rendering based on page mode
if page_mode == "💬 Chat":
    st.header("Chat with GestureGPT")
    st.markdown("Send messages and receive responses in sign language!")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "user_input_asl" in message and message["user_input_asl"]:
                st.info(f"💡 **Your message in ASL:** {message['user_input_asl']}")
            if "video_urls" in message:
                # Display videos in a grid layout
                num_videos = len(message["video_urls"])
                if num_videos > 0:
                    # Create columns based on number of videos (max 4 per row)
                    cols_per_row = min(4, num_videos)

                    for i in range(0, num_videos, cols_per_row):
                        cols = st.columns(cols_per_row)
                        for j, video_url in enumerate(message["video_urls"][i:i+cols_per_row]):
                            with cols[j]:
                                render_video(video_url, autoplay=autoplay, max_size=size_px)
            if "missing_videos" in message and message["missing_videos"]:
                st.warning(f"⚠️ Videos not available for: {', '.join(message['missing_videos'])}")

    # Chat input - MUST be last element on page
    if prompt := st.chat_input("Type your message..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Show loading message
        with st.chat_message("assistant"):
            with st.spinner("Thinking and generating sign language..."):
                # Call API
                try:
                    api_messages = [
                        {"role": msg["role"], "content": msg["content"]}
                        for msg in st.session_state.messages
                    ]

                    response = requests.post(
                        f"{GESTUREGPT_URL}/v1/chat/completions",
                        json={
                            "model": "gesturegpt-v1",
                            "messages": api_messages,
                            "format": video_format
                        },
                        timeout=30
                    )

                    if response.status_code == 200:
                        data = response.json()
                        assistant_message = data["choices"][0]["message"]["content"]
                        video_urls = data["choices"][0].get("video_urls", [])
                        missing_videos = data["choices"][0].get("missing_videos", [])
                        user_input_asl = data["choices"][0].get("user_input_asl")

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": assistant_message,
                            "video_urls": video_urls,
                            "missing_videos": missing_videos,
                            "user_input_asl": user_input_asl
                        })
                    else:
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"API Error: {response.status_code}",
                            "video_urls": [],
                            "missing_videos": []
                        })

                except Exception as e:
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Error: {str(e)}",
                        "video_urls": [],
                        "missing_videos": []
                    })

        st.rerun()

elif page_mode == "🎯 Direct Conversion":
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
                    f"{GESTUREGPT_URL}/api/sign-language/generate",
                    json={
                        "text": text_input,
                        "format": video_format
                    },
                    timeout=30
                )

                if response.status_code == 200:
                    data = response.json()

                    st.success("✅ Videos generated successfully!")

                    # Show original and normalized text
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("### Original Text")
                        st.info(data.get('text', ''))
                    with col2:
                        st.markdown("### Normalized Text")
                        st.info(data.get('normalized_text', ''))

                    # Display videos with autoplay
                    st.markdown("### Generated Videos")
                    video_urls = data.get("video_urls", [])

                    if video_urls:
                        # Display videos in a grid layout
                        num_videos = len(video_urls)
                        cols_per_row = min(4, num_videos)

                        for i in range(0, num_videos, cols_per_row):
                            cols = st.columns(cols_per_row)
                            for j, video_url in enumerate(video_urls[i:i+cols_per_row]):
                                with cols[j]:
                                    render_video(video_url, autoplay=autoplay, max_size=size_px)
                    else:
                        st.warning("No videos available")

                    # Show missing videos warning
                    missing_videos = data.get("missing_videos", [])
                    if missing_videos:
                        st.warning(f"⚠️ Videos not available for: {', '.join(missing_videos)}")

                    # Display metadata
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Videos Found", len(video_urls))
                    with col2:
                        st.metric("Format", data.get('format', 'N/A').upper())
                    with col3:
                        st.metric("Status", "✅ Success" if data.get('success') else "⚠️ Partial")

                else:
                    st.error(f"API Error: {response.status_code}")
                    st.json(response.json())

            except Exception as e:
                st.error(f"Error: {str(e)}")

    elif generate_button and not text_input:
        st.warning("⚠️ Please enter some text first!")

elif page_mode == "📚 API Docs":
    st.header("API Documentation")

    st.markdown("""
    ### OpenAI-Compatible Chat Endpoint

    **POST** `/v1/chat/completions`

    ```python
    import requests

    response = requests.post(
        "http://localhost:8000/v1/chat/completions",
        json={
            "model": "gesturegpt-v1",
            "messages": [
                {"role": "user", "content": "Hello, how are you?"}
            ],
            "format": "mp4"
        }
    )

    # Response includes video_urls array
    data = response.json()
    video_urls = data["choices"][0]["video_urls"]
    missing_videos = data["choices"][0].get("missing_videos", [])
    ```

    ### Direct Sign Language Endpoint

    **POST** `/api/sign-language/generate`

    ```python
    response = requests.post(
        "http://localhost:8000/api/sign-language/generate",
        json={
            "text": "Hello, how are you?",
            "format": "mp4"
        }
    )

    # Response includes multiple video URLs
    data = response.json()
    for video_url in data["video_urls"]:
        print(video_url)
    ```

    ### Using with OpenAI Python SDK

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

    # Access video URLs from response
    print(response.choices[0].video_urls)
    ```
    """)

    st.divider()

    st.markdown("### Available Models")
    try:
        models_response = requests.get(f"{GESTUREGPT_URL}/v1/models", timeout=5)
        if models_response.status_code == 200:
            st.json(models_response.json())
        else:
            st.error("Failed to fetch models")
    except:
        st.error("API unavailable")
