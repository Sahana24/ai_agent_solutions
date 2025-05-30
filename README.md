# English Accent Classifier

🔗 **Live App**: [Try it on Streamlit Cloud](https://aiagentsolutions-ae7mq89xptagsiou6t4czc.streamlit.app/)

## What Is This?

This tool helps evaluate the spoken English proficiency of candidates for hiring or screening purposes. It analyzes the speaker’s voice from a public video and estimates their English accent, along with a confidence score and visual summary.

## Features

- **Video Input:** Accepts public video URLs (Loom, YouTube, or direct MP4 links).
- **Audio Extraction:** Converts video to audio using ffmpeg.
- **Language Check:** Uses OpenAI Whisper to check if the audio is in English.
- **Accent Classification:** Compares the speaker's voice to a set of reference accents (British, American, Australian, etc.) using SpeechBrain embeddings.
- **Confidence Scoring:** Provides a confidence score (0–100%) for the detected accent.
- **User-Friendly UI:** Built with Streamlit for easy testing and deployment.

## Tech Stack

- [Streamlit](https://streamlit.io/) – Interactive web UI
- [SpeechBrain](https://speechbrain.readthedocs.io/) – Speaker embedding extraction using ECAPA-TDNN
- [Whisper](https://openai.com/research/whisper) – Speech-to-text and language detection
- [FFmpeg](https://ffmpeg.org/) – Audio extraction from video
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) – Video downloader for YouTube and other sources

## Project Structure

```
ai_agent_solutions/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── reference_embeddings.pkl  # Pre-computed accent embeddings
├── utils/                 # Utility modules
│   ├── downloader.py      # Video download and audio extraction
│   ├── transcription.py   # Speech-to-text and language detection
│   ├── embedding.py       # Speaker embedding extraction
│   ├── classifier.py      # Accent classification logic
│   └── generate_reference_embeddings.py  # Generate accent embeddings
├── reference_accents/     # Reference audio samples
│   ├── american/         # US English samples
│   ├── british/          # UK English samples
│   ├── australian/       # Australian English samples
│   ├── indian/           # Indian English samples
│   ├── nigerian/         # Nigerian English samples
│   ├── canadian/         # Canadian English samples
│   └── scottish/         # Scottish English samples
├── static/               # Static assets
│   └── accent_classifier_01.png  # UI screenshot
└── downloads/            # Temporary storage for processed files
```

## Getting Started

### Prerequisites

- Python 3.11
- FFmpeg installed on your system
  - Download from [ffmpeg.org](https://ffmpeg.org/download.html)
  - Make sure it's added to your system PATH

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Sahana24/ai_agent_solutions.git
   cd ai_agent_solutions
   ```
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Open the app in your browser.
2. Paste a public video URL into the input field (YouTube, Loom, or direct .mp4 link).
3. Click Run Analysis.
4. View the results:
   - Detected accent
   - Confidence score
   - Short explanation
   - Bar chart of accent confidence scores

## Dataset

The tool uses a curated set of reference audio clips from the **[Common Voice Corpus 21.0 (English)](https://commonvoice.mozilla.org/en/datasets)** developed by Mozilla. This is a large, open-source, multilingual dataset containing voice recordings from diverse speakers around the world.

For this project, we selected samples labeled with the following English accents:
- **American (United States English)**
- **British (England English)**
- **Australian English**
- **Indian English**
- **Nigerian English**
- **Canadian English**
- **Scottish English**

Each accent category contains up to **1-3 validated audio clips** (in `.mp3` format), which are converted to **16kHz mono `.wav` files** and stored in the `reference_accents/` directory. These clips serve as **reference anchors** for accent comparison.

We use **SpeechBrain's pre-trained speaker embedding model** (`ecapa-tdnn`) to convert these clips into fixed-size vector embeddings. During analysis, the speaker's embedding is compared against these reference embeddings using cosine similarity to classify the accent and score the confidence.

> ⚠️ Note: Some accents may have fewer than 3 available clips in the dataset due to limited contributions for those categories.

## Screenshots

Here's what the app looks like in action:

![Accent Classifier UI](static/accent_classifier_01.png)

*The app shows the detected accent, confidence score, and a bar chart of accent confidence scores.*

## Credits

- Mozilla Common Voice – Open speech dataset
- OpenAI Whisper – Language detection
- SpeechBrain – Speaker embedding model
- Streamlit – Web app framework
- FFmpeg – Audio/video processing

## License

This project is for educational and evaluation purposes only.

---

Feel free to reach out if you have any questions or need help! 