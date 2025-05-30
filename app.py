import streamlit as st
from utils.downloader import download_video, extract_audio
from utils.transcription import transcribe_and_check_language
from utils.embedding import extract_speaker_embedding, load_reference_embeddings
from utils.classifier import classify_accent
import matplotlib.pyplot as plt

st.title("🎙️ English Accent Classifier")
st.write("Paste a video URL (Loom, YouTube, or direct .mp4) to analyze the speaker's accent.")

with st.form("accent_form"):
    video_url = st.text_input("Video URL")
    submit = st.form_submit_button("Run Analysis")

if submit and video_url:
    try:
        st.info("Analysis started. Please wait...")
        with st.spinner("Downloading video..."):
            video_path = download_video(video_url)  # Download video from URL
        with st.spinner("Extracting audio..."):
            audio_path = extract_audio(video_path)  # Extract audio to WAV
        with st.spinner("Transcribing and detecting language..."):
            lang = transcribe_and_check_language(audio_path)  # Check if English

        if lang != "en":
            st.error("Non-English language detected. Skipping accent analysis.")  # Skip if not English
        else:
            with st.spinner("Classifying accent..."):
                ref_db = load_reference_embeddings()  # Load reference accent embeddings
                embedding = extract_speaker_embedding(audio_path)  # Get speaker embedding
                accent, confidence, scores = classify_accent(embedding, ref_db)  # Classify accent

            st.success("Analysis complete!")
            st.markdown(f"**Detected Accent:** `{accent}`")
            st.markdown(f"**Confidence Score:** `{confidence}%`")

            if confidence > 80:
                summary = (
                    f"The model is highly confident that the speaker has a **{accent}** English accent. "
                    "The voice closely matches known patterns in our reference samples."
                )
            elif confidence > 50:
                summary = (
                    f"The model suggests the speaker likely has a **{accent}** English accent, "
                    "but the result is moderately confident. This may be due to background noise, speaker variability, or regional overlap."
                )
            else:
                summary = (
                    f"The model detected some features of a **{accent}** English accent, "
                    "but with low confidence. The speaker's pronunciation may be atypical or underrepresented in our training examples."
                )

            st.info(summary)  # Display summary based on confidence
            
            st.subheader("Accent Confidence Scores")
            sorted_scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))  # Sort scores for display
            fig, ax = plt.subplots()
            bars = ax.bar(range(len(sorted_scores)), sorted_scores.values(), color="#B19CD9")
            ax.set_xticks(range(len(sorted_scores)))
            ax.set_xticklabels([accent.capitalize() for accent in sorted_scores.keys()], rotation=30)
            ax.set_ylabel("Confidence (%)")
            ax.set_ylim(0, 110)
            ax.set_title("Similarity to Known Accent Profiles")

            # Add value labels on top of bars
            for i, value in enumerate(sorted_scores.values()):
                ax.text(i, value + 1, f"{value:.1f}%", ha='center', va='bottom', fontsize=9)

            st.pyplot(fig)
            st.caption("Accent estimated by comparing speaker embedding to reference profiles.")

    except Exception as e:
        st.error(f"Something went wrong: `{str(e)}`")  # Catch and display any errors
