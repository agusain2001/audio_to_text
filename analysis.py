import re

# Define a list of common filler words
FILLER_WORDS = ["um", "uh", "like", "you know", "so", "actually", "basically", "I mean"]

def count_filler_words(text):
    """
    Counts occurrences of defined filler words in the transcript.
    Returns a dictionary mapping each filler word to its count.
    """
    words = re.findall(r"\w+", text.lower())
    filler_counts = {word: 0 for word in FILLER_WORDS}
    for w in words:
        if w in filler_counts:
            filler_counts[w] += 1
    return filler_counts

def detect_monologues(text, diarization):
    """
    Groups continuous speech segments (monologues) using diarization data.
    If diarization is not available, returns the full transcript.
    """
    if diarization:
        monologues = []
        current_speaker = None
        current_text = ""
        for word, speaker in diarization:
            if current_speaker is None:
                current_speaker = speaker
            if speaker == current_speaker:
                current_text += word + " "
            else:
                monologues.append(current_text.strip())
                current_text = word + " "
                current_speaker = speaker
        if current_text:
            monologues.append(current_text.strip())
        return monologues
    else:
        return [text]

def compute_pace(text, duration):
    """
    Calculates words per minute (wpm) and categorizes the pace:
      - wpm < 100: slow
      - 100 <= wpm <= 150: normal
      - wpm > 150: fast
    """
    words = text.split()
    total_words = len(words)
    minutes = duration / 60.0
    wpm = total_words / minutes if minutes > 0 else total_words
    if wpm < 100:
        pace = "slow"
    elif wpm > 150:
        pace = "fast"
    else:
        pace = "normal"
    return pace, wpm
