# transcribe.py
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio(file_path: str) -> str | None:
    """Send an audio file to OpenAI Whisper and return the transcript text."""
    try:
        with open(file_path, "rb") as audio_file:
            transcript_obj = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )
        return transcript_obj.text
    except Exception as e:
        print(f"[Transcribe] Error: {e}")
        return None
