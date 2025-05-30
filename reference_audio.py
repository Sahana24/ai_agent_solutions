import pandas as pd
import os
import shutil
import subprocess

# Load validated.tsv from Common Voice
TSV_PATH = r"dataset\cv-corpus-21.0-delta-2025-03-14-en\cv-corpus-21.0-delta-2025-03-14\en\validated.tsv"
CLIPS_DIR = r"dataset\cv-corpus-21.0-delta-2025-03-14-en\cv-corpus-21.0-delta-2025-03-14\en\clips"
df = pd.read_csv(TSV_PATH, sep="\t")

# Create reference accents directory
os.makedirs("reference_accents", exist_ok=True)

# Define your list of accents and their keywords/accent names
ACCENT_MAP = {
    "american": "united states",
    "british": "england",
    "australian": "australian",
    "indian": "india",
    "nigerian": "nigerian",
    "canadian": "canadian",
    "scottish": "scottish",
}

# Function to extract, convert, and save reference audio clips as WAV
def save_clips(accent_keyword, label, n=3):
    subset = df[df['accents'].fillna('').str.lower().str.contains(accent_keyword.lower())]
    samples = subset.head(n)
    target_dir = f"reference_accents/{label}"
    os.makedirs(target_dir, exist_ok=True)

    for i, row in samples.iterrows():
        filename = row["path"]
        src = os.path.join(CLIPS_DIR, filename)
        dst_wav = os.path.join(target_dir, f"{label}_{i}.wav")

        if os.path.exists(src):
            # Convert directly to WAV 16kHz mono
            cmd = ["ffmpeg", "-y", "-i", src, "-ar", "16000", "-ac", "1", dst_wav]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"Converted to WAV: {dst_wav}")
        else:
            print(f"Missing file: {src}")

# Loop through accents
for label, keyword in ACCENT_MAP.items():
    save_clips(keyword, label, n=3)

print("All reference accents prepared as WAV files.")