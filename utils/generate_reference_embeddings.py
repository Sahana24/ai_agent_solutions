import os
import numpy as np
from tqdm import tqdm
from speechbrain.inference.speaker import EncoderClassifier
import torchaudio
import pickle

# Paths
REFERENCE_DIR = "reference_accents"  # Directory containing reference accent audio files
OUTPUT_FILE = "reference_embeddings.pkl"  # Output file for reference embeddings

# Initialize model
classifier = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb")  # Load SpeechBrain model

# Dictionary to hold embeddings: {"accent": [embeddings]}
reference_db = {}

for accent in os.listdir(REFERENCE_DIR):
    accent_dir = os.path.join(REFERENCE_DIR, accent)
    if not os.path.isdir(accent_dir):
        continue

    embeddings = []
    for file in tqdm(os.listdir(accent_dir), desc=f"Processing {accent}"):  # Process each audio file
        if not file.endswith(".wav"):
            continue
        path = os.path.join(accent_dir, file)
        signal, fs = torchaudio.load(path)  # Load audio file
        embedding = classifier.encode_batch(signal).squeeze().detach().cpu().numpy()  # Extract embedding
        embeddings.append(embedding)

    if embeddings:
        reference_db[accent] = np.stack(embeddings)  # Stack embeddings for this accent

# Save embeddings as pickle
with open(OUTPUT_FILE, "wb") as f:
    pickle.dump(reference_db, f)  # Save reference embeddings to pickle file

print(f"Saved reference embeddings to {OUTPUT_FILE}")
