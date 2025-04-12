# YouTube Video Summarizer Agent - Using Groq API via LangChain + Streamlit UI + Whisper + yt_dlp
# Requirements: pip install yt-dlp openai-whisper streamlit pydub python-dotenv langchain langchain-community

import os
import subprocess
import whisper
import streamlit as st
import math
from dotenv import load_dotenv
from pydub import AudioSegment
from yt_dlp import YoutubeDL
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage

load_dotenv()

# Config
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")
MAX_CHUNK_LENGTH = int(os.getenv("MAX_CHUNK_LENGTH", "1800"))
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "medium")

# Download audio using yt_dlp
def download_audio(url, output_path="downloads"):
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(id)s.%(ext)s'),
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = os.path.join(output_path, f"{info['id']}.mp3")
            return file_path, info.get("title", "Unknown Video"), int(info.get("duration", 0))

    except Exception as e:
        raise Exception(f"Error downloading video: {str(e)}")

# Check if ffmpeg is installed
def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except Exception:
        return False

# Split audio into chunks
def split_audio(audio_path, chunk_length=MAX_CHUNK_LENGTH):
    if not check_ffmpeg():
        raise Exception("FFmpeg is not installed or not in PATH.")

    audio = AudioSegment.from_file(audio_path)
    chunks = []
    total_chunks = math.ceil(len(audio) / (chunk_length * 1000))

    for i in range(total_chunks):
        start = i * chunk_length * 1000
        end = min((i + 1) * chunk_length * 1000, len(audio))
        chunk = audio[start:end]
        chunk_path = f"{audio_path}_chunk_{i}.mp3"
        chunk.export(chunk_path, format="mp3")
        chunks.append(chunk_path)

    return chunks

# Transcribe
def transcribe_audio(audio_path):
    model = whisper.load_model(WHISPER_MODEL)
    result = model.transcribe(audio_path)
    return result['text']

# Summarize using LangChain + Groq
def summarize_with_groq(transcript, is_chunk=False, chunk_number=None, total_chunks=None):
    chunk_info = f"\n[Part {chunk_number}/{total_chunks}]" if is_chunk else ""

    prompt = f"""
You are an intelligent educational summarizer. Here's a transcript of a YouTube video{chunk_info}. Your task is to:

1. Provide a concise summary.
2. Explain key concepts.
3. Extract and explain all formulas clearly.
4. Highlight examples or tips.
5. List final takeaways for learners.

Format:
🔹 Video Summary  
📘 Key Concepts Explained  
🧮 Important Formulas (with explanations)  
💡 Tips & Examples  
✅ Final Learnings / Takeaways  

Transcript:
{transcript}
"""

    chat = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    )
    messages = [
        SystemMessage(content="You are a helpful educational assistant."),
        HumanMessage(content=prompt)
    ]
    response = chat.invoke(messages)
    return response.content

# Combine summaries
def combine_summaries(summaries):
    combined_prompt = """
You are an intelligent educational summarizer. Below are summaries of different parts of a YouTube video. 
Please combine them into a coherent, comprehensive summary that:

1. Eliminates redundancies
2. Maintains a logical flow
3. Preserves all important information
4. Provides a unified summary of the entire video

Summaries to combine:
"""

    for i, summary in enumerate(summaries, 1):
        combined_prompt += f"\n\n=== Part {i} ===\n{summary}"

    return summarize_with_groq(combined_prompt)

# Run agent
def run_agent(youtube_url):
    audio_file = None
    chunk_files = []
    try:
        audio_file, title, duration = download_audio(youtube_url)

        if duration > MAX_CHUNK_LENGTH:
            chunk_files = split_audio(audio_file)
            summaries = []

            for i, chunk in enumerate(chunk_files, 1):
                transcript = transcribe_audio(chunk)
                summary = summarize_with_groq(transcript, is_chunk=True, chunk_number=i, total_chunks=len(chunk_files))
                summaries.append(summary)
                os.remove(chunk)

            final_summary = combine_summaries(summaries)
        else:
            transcript = transcribe_audio(audio_file)
            final_summary = summarize_with_groq(transcript)

        return final_summary

    except Exception as e:
        raise Exception(f"Error: {str(e)}")

    finally:
        if audio_file and os.path.exists(audio_file):
            os.remove(audio_file)
        for chunk in chunk_files:
            if os.path.exists(chunk):
                os.remove(chunk)

if __name__ == "__main__":
    url = input("Enter YouTube video URL: ")
    print(run_agent(url))