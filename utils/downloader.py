import os
import subprocess
import uuid
import requests

def download_video(url: str, output_dir="downloads") -> str:
    os.makedirs(output_dir, exist_ok=True)  # Create output directory if it doesn't exist
    temp_id = uuid.uuid4().hex  # Generate a unique filename
    video_path = os.path.join(output_dir, f"{temp_id}.mp4")

    if "youtube.com" in url or "youtu.be" in url:
        # Use yt-dlp for YouTube
        cmd = ["yt-dlp", "-f", "mp4", "-o", video_path, url]
        subprocess.run(cmd, check=True)
    else:
        # Handle direct MP4 (e.g., Loom)
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(video_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        else:
            raise Exception(f"Failed to download video from URL. Status code: {response.status_code}")

    return video_path

def extract_audio(video_path: str, output_dir="downloads") -> str:
    audio_path = video_path.replace(".mp4", ".wav")  # Convert MP4 to WAV
    cmd = ["ffmpeg", "-y", "-i", video_path, "-t", "120", "-ar", "16000", "-ac", "1", audio_path]  # Extract 120s of audio, 16kHz mono
    subprocess.run(cmd, check=True)
    os.remove(video_path)  # Clean up the video file
    return audio_path
