# Audio Analysis Project

## Overview

The Audio Analysis Project is a modular Python application that processes audio files to extract valuable insights. It performs the following tasks:

- **Audio Transcription:** Converts audio into text using [Google Cloud Speech-to-Text](https://cloud.google.com/speech-to-text) with speaker diarization.
- **Text Analysis:** Analyzes the transcript to detect filler words, identify monologues, and compute the speaker's pace.
- **Text Generation:** Uses Google Gemini deployed on [Vertex AI](https://cloud.google.com/vertex-ai) to generate a summary, produce alternative rewritten versions, and extract keywords from the transcript.

This project demonstrates how to integrate multiple Google Cloud services into a robust and scalable audio processing pipeline.

## Features

- **Accurate Transcription:** Leverages Google Cloud Speech-to-Text for reliable audio-to-text conversion.
- **Detailed Analysis:** Counts common filler words, segments continuous speech (monologues), and calculates words per minute.
- **Advanced Text Generation:** Generates summaries, rewrites the transcript in different styles, and extracts keywords using Vertex AI.
- **Modular Design:** Clear separation of concerns with distinct modules for audio processing, analysis, and text generation.
- **Command-Line Interface:** Easily specify the audio file to process via command-line arguments.

## Requirements

- Python 3.7 or higher
- Google Cloud Speech-to-Text API enabled
- Google Cloud Vertex AI with a deployed Gemini model
- Google Cloud credentials (configured via the `GOOGLE_APPLICATION_CREDENTIALS` environment variable)
- Required Python packages (listed in [requirements.txt](requirements.txt))

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/agusain2001/audio_to_text.git
   cd audio_analysis_project
   ```

2. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure Google Cloud Credentials**
    - Ensure you have a service account with the necessary permissions. Set the environment variable:
    - ```bash
        export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json" 
        ```
4. **Update Configuration:**
Edit the config.py file with your Google Cloud project details, including:

- GOOGLE_CLOUD_PROJECT
- PROJECT_ID
- LOCATION (e.g., us-central1)
- GEMINI_ENDPOINT_ID (Vertex AI endpoint ID for your Gemini model)

## Usage
Run the project from the command line by specifying an audio file:
    ```bash
        python main.py --audio_file path/to/your_audio.wav
    ```
The application will:
- Transcribe the audio file.
- Analyze the transcript for filler words, monologues, and speaker pace.
- Generate a summary, alternative rewritten versions, and extract keywords using Vertex AI.

## File Structure

    ```bash
    audio_analysis_project/
    ├── main.py                # Main entry point to coordinate the workflow
    ├── config.py              # Configuration settings (API keys, project IDs, endpoints, etc.)
    ├── audio_processor.py     # Handles audio transcription and duration calculation
    ├── analysis.py            # Analyzes the transcript for filler words, monologues, and pace
    ├── text_generation.py     # Uses Vertex AI for text generation (summary, rewriting, keyword extraction)
    └── requirements.txt       # List of required packages
    ```
## TroubleShooting
- **Transcription Errors**: Ensure the audio file is in the proper format (e.g., LINEAR16 encoding) and that the sample rate in audio_processor.py matches your audio file.
- **Vertex AI Errors**: Verify that your Gemini model is deployed on Vertex AI and that the endpoint ID is correct in config.py.
- **Credential Issues**: Double-check that your GOOGLE_APPLICATION_CREDENTIALS environment variable points to the correct service account JSON file.
