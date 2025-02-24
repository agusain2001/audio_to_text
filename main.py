import argparse
import logging
from audio_processor import transcribe_audio, get_audio_duration
from analysis import count_filler_words, detect_monologues, compute_pace
from text_generation import summarize_text, rewrite_text, generate_keywords

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def parse_args():
    parser = argparse.ArgumentParser(description="Audio Analysis Project")
    parser.add_argument(
        "--audio_file",
        type=str,
        default="sample_audio.wav",
        help="Path to the audio file to process."
    )
    return parser.parse_args()

def main():
    setup_logging()
    args = parse_args()

    try:
        logging.info("Starting audio transcription...")
        transcript, diarization = transcribe_audio(args.audio_file)
        logging.info("Audio transcription completed.")
    except Exception as e:
        logging.error(f"Error during transcription: {e}")
        return

    try:
        duration = get_audio_duration(args.audio_file)
    except Exception as e:
        logging.error(f"Error obtaining audio duration: {e}")
        return

    logging.info("=== Transcript ===")
    logging.info(transcript)

    # Analyze filler words
    filler_counts = count_filler_words(transcript)
    logging.info("=== Filler Words Count ===")
    for word, count in filler_counts.items():
        logging.info(f"{word}: {count}")

    # Detect monologues
    monologues = detect_monologues(transcript, diarization)
    logging.info("=== Detected Monologues ===")
    for idx, mono in enumerate(monologues):
        logging.info(f"Monologue {idx+1}: {mono[:100]}...")  # Preview first 100 characters

    # Compute pace
    pace_category, wpm = compute_pace(transcript, duration)
    logging.info("=== Speaker Pace ===")
    logging.info(f"Pace: {pace_category} (Words per minute: {wpm:.2f})")

    # Generate summary via Vertex AI
    try:
        summary = summarize_text(transcript)
        logging.info("=== Audio Summary ===")
        logging.info(summary)
    except Exception as e:
        logging.error(f"Error generating summary: {e}")

    # Generate rewritten versions
    logging.info("=== Rewritten Versions ===")
    for i in range(1, 4):
        try:
            rewritten = rewrite_text(transcript, variant=i)
            logging.info(f"Version {i}:")
            logging.info(rewritten)
        except Exception as e:
            logging.error(f"Error generating rewritten version {i}: {e}")

    # Extract keywords
    try:
        keywords = generate_keywords(transcript, num_keywords=5)
        logging.info("=== Extracted Keywords ===")
        logging.info(", ".join(keywords))
    except Exception as e:
        logging.error(f"Error extracting keywords: {e}")

if __name__ == "__main__":
    main()
