# YouTube Video Summarizer Agent

This project is a **YouTube Video Summarizer Agent** that takes a YouTube video URL, downloads the audio, transcribes it, and provides a detailed summary of the video. It uses **Whisper** for transcription and **Groq API** for summarization. The project also integrates with **Streamlit** for a simple web interface.

## Requirements

- Python 3.7+
- You will need to install the following Python dependencies:

```bash
pip install -r requirements.txt
## 📁 Environment Variables (.env)

This project uses a `.env` file to securely manage API keys and configuration.  
You **must** create this file in the root of the project before running the code.

### 👉 Create a `.env` file and add the following:

```env
# .env file for storing sensitive environment variables

# Groq API key for summarization
GROQ_API_KEY=your_groq_api_key

# Groq Model to use (check Groq dashboard for available models)
GROQ_MODEL=llama3-8b-8192

# Whisper Model to use (tiny, base, small, medium, large)
WHISPER_MODEL=medium

# Max Chunk Length in seconds for audio processing (default 1800 = 30 minutes)
MAX_CHUNK_LENGTH=1800

