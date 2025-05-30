import whisper

model = whisper.load_model("base")  # Load Whisper model for transcription

def transcribe_and_check_language(audio_path: str) -> str:
    result = model.transcribe(audio_path)  # Transcribe audio to text
    language = result.get("language")  # Extract detected language
    return language