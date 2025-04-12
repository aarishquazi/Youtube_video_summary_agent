import streamlit as st
import os
from youtube_summarizer import run_agent
import time
from datetime import timedelta

# Page configuration
st.set_page_config(
    page_title="YouTube Video Summarizer",
    page_icon="📺",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .main-header {
        text-align: center;
        color: #FF0000;
        font-size: 2.5em;
        margin-bottom: 1em;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2em;
        margin-bottom: 2em;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1em;
        border-radius: 10px;
        margin: 1em 0;
    }
    .summary-box {
        background-color: #ffffff;
        padding: 2em;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1em 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">YouTube Video Summarizer</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Transform long YouTube videos into concise, educational summaries</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    # Model selection
    whisper_model = st.selectbox(
        "Whisper Model",
        ["tiny", "base", "small", "medium", "large"],
        index=3,
        help="Select the Whisper model for transcription. Larger models are more accurate but slower."
    )
    
    # Chunk length
    chunk_length = st.slider(
        "Chunk Length (minutes)",
        min_value=15,
        max_value=60,
        value=30,
        step=15,
        help="Length of video chunks for processing. Longer chunks take more memory but fewer API calls."
    )
    
    # Groq model selection
    groq_model = st.selectbox(
        "Groq Model",
        ["mistral-saba-24b", "llama-3.3-70b-versatile", "gemma-7b-it"],
        index=0,
        help="Select the Groq model for summarization."
    )
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    This tool uses:
    - Whisper for accurate transcription
    - Groq for intelligent summarization
    - Advanced chunking for long videos
    
    Made with ❤️ for educational content
    """)

# Main content
st.markdown("### 📝 Enter YouTube URL")
url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...", label_visibility="collapsed")

if url:
    # Create a progress container
    progress_container = st.empty()
    summary_container = st.empty()
    
    try:
        # Update configuration
        os.environ["WHISPER_MODEL"] = whisper_model
        os.environ["MAX_CHUNK_LENGTH"] = str(chunk_length * 60)  # Convert to seconds
        os.environ["GROQ_MODEL"] = groq_model
        
        # Show processing message
        with progress_container:
            st.info("🔄 Processing video... This may take a few minutes depending on the video length.")
            
            # Create progress bars
            download_progress = st.progress(0)
            transcribe_progress = st.progress(0)
            summarize_progress = st.progress(0)
            
            # Status messages
            status = st.empty()
        
        # Run the summarizer
        with summary_container:
            summary = run_agent(url)
            
            # Format the summary with markdown
            st.markdown("### 📊 Summary")
            st.markdown(summary)
            
            # Add download button for the summary
            st.download_button(
                label="📥 Download Summary",
                data=summary,
                file_name="video_summary.md",
                mime="text/markdown"
            )
            
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("Please check the URL and try again.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Made with Streamlit • Powered by Whisper & Groq</p>
</div>
""", unsafe_allow_html=True) 