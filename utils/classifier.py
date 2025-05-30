from scipy.spatial.distance import cosine
import numpy as np

def classify_accent(embedding, reference_db: dict) -> tuple:
    raw_scores = {}  # Store raw similarity scores for each accent

    for accent, ref_embeddings in reference_db.items():
        similarities = [
            1 - cosine(embedding, ref_emb) for ref_emb in ref_embeddings  # Compute cosine similarity
        ]
        raw_scores[accent] = np.mean(similarities)  # Average similarity for this accent

    # Normalize to 0–100%
    min_score = min(raw_scores.values())
    max_score = max(raw_scores.values())
    normalized_scores = {
        accent: round(100 * (score - min_score) / (max_score - min_score + 1e-5), 2)  # Normalize and round
        for accent, score in raw_scores.items()
    }

    best = max(normalized_scores, key=normalized_scores.get)  # Get the best matching accent
    return best.capitalize(), normalized_scores[best], normalized_scores  # Return best accent, its score, and all scores
