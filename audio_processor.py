import io
import wave
import logging
from google.cloud import speech

def transcribe_audio(file_path):
    """
    Transcribes the audio file using Google Cloud Speech-to-Text with speaker diarization.
    Returns the full transcript and diarization data (list of tuples: (word, speaker_tag)).
    """
    try:
        client = speech.SpeechClient()
    except Exception as e:
        logging.error("Failed to create SpeechClient. Ensure your Google Cloud credentials are set.")
        raise e

    try:
        with io.open(file_path, "rb") as audio_file:
            content = audio_file.read()
    except Exception as e:
        logging.error(f"Error reading audio file: {file_path}")
        raise e

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,  # Adjust if needed
        language_code="en-US",
        enable_speaker_diarization=True,
        diarization_speaker_count=2  # Adjust based on expected speakers
    )

    try:
        response = client.recognize(config=config, audio=audio)
    except Exception as e:
        logging.error("Error during speech recognition.")
        raise e

    transcript = ""
    diarization = []  # List of tuples (word, speaker_tag)
    for result in response.results:
        alternative = result.alternatives[0]
        transcript += alternative.transcript + " "
        if hasattr(alternative, 'words'):
            for word_info in alternative.words:
                diarization.append((word_info.word, word_info.speaker_tag))
    return transcript.strip(), diarization

def get_audio_duration(file_path):
    """
    Returns the duration of the audio file in seconds.
    """
    try:
        with wave.open(file_path, 'rb') as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            duration = frames / float(rate)
        return duration
    except Exception as e:
        logging.error("Error obtaining audio duration.")
        raise e
