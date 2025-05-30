import numpy as np
import os
import pickle
from speechbrain.inference.speaker import EncoderClassifier
import torchaudio

# Initialize model only once
classifier = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb")  # Load SpeechBrain model for speaker embedding

# Load precomputed reference embeddings
REFERENCE_EMBEDDINGS_PATH = "reference_embeddings.pkl"

def load_reference_embeddings():
    if not os.path.exists(REFERENCE_EMBEDDINGS_PATH):
        raise FileNotFoundError(f"Reference embedding file not found: {REFERENCE_EMBEDDINGS_PATH}")  # Check if file exists

    with open(REFERENCE_EMBEDDINGS_PATH, "rb") as f:
        return pickle.load(f)  # Load reference embeddings from pickle file

def extract_speaker_embedding(audio_path):
    signal, fs = torchaudio.load(audio_path)  # Load audio file
    embedding = classifier.encode_batch(signal).squeeze().detach().cpu().numpy()  # Extract speaker embedding
    return embedding