# YouTube Video Summarizer Agent

This project is a **YouTube Video Summarizer Agent** that takes a YouTube video URL, downloads the audio, transcribes it, and provides a detailed summary of the video. It uses **Whisper** for transcription and **Groq API** for summarization. The project also integrates with **Streamlit** for a simple web interface.

---

## ✅ Requirements

- Python 3.7+
- Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 📁 Environment Variables (.env)

This project uses a `.env` file to securely manage API keys and configuration. You **must** create this file in the root of the project before running the code.

### 👉 Create a `.env` file and add the following:

```env
# Groq API key
GROQ_API_KEY=your_groq_api_key

# Groq model (e.g., llama3-8b-8192 or others from Groq Console)
GROQ_MODEL=llama3-8b-8192

# Whisper model to use for transcription (tiny, base, small, medium, large)
WHISPER_MODEL=medium

# Max duration (in seconds) for audio chunking
MAX_CHUNK_LENGTH=1800
```

✅ Make sure `.env` is included in `.gitignore` to prevent accidental exposure of your API key.

---

## 🏃‍♂️ How to Run the Code

Follow the steps below to set up and run the **YouTube Video Summarizer Agent**:

---

### 1. 📦 Clone the Repository

```bash
git clone https://github.com/yourusername/youtube-summarizer-agent.git
cd youtube-summarizer-agent
```

---

### 2. 🧪 Create Virtual Environment and Activate

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

---

### 3. 📥 Install Required Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. 🔐 Set Up `.env` File

Create a `.env` file in the root directory of the project and add the variables shown in the section above.

---

### 5. ▶️ Run the App

```bash
streamlit run app.py
```

Open the provided URL (typically `http://localhost:8501`) in your browser and paste any **YouTube video URL** to generate a smart summary.

---
