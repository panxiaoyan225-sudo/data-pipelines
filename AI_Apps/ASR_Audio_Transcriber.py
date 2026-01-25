# Whisper is an open-source automatic speech recognition (ASR) system created by OpenAI.
# It can transcribe spoken language in audio files to text, and supports multiple languages.
# Below, we import the 'whisper' library to access its transcription models and functions.
#import TextToAudio
import whisper
import os
from dotenv import load_dotenv, find_dotenv
import os
# 1. LOAD CONFIGURATION
# find_dotenv() must have () to work correctly
# MySQL credentials
load_dotenv(find_dotenv())
# Fetching all components from .env
# 2. Get the base path from the environment variable
base_path = os.getenv("MY_PROJECT_PATH")

def transcribe_audio(file_path):
    """
    Transcribe speech from an audio file using OpenAI's Whisper ASR.
    Args:
        file_path (str): Path to the audio file.
    Returns:
        str: Transcribed text, or error message if file is not found.
    """
    if not os.path.exists(file_path):
        return "File not found."

    # Load model only once for efficiency
    model = whisper.load_model("base")
    print(f"Transcribing: {file_path}...")
    result = model.transcribe(file_path)
    return result.get("text", "")
     # Extract the 'text' key from the result dictionary, which contains the transcription.
    # If the 'text' key doesn't exist, return an empty string as a fallback.

# The following block ensures that the enclosed code only executes when this script is run directly,
# and not when it is imported as a module in another script. This is a common Python idiom for providing
# code that is meant to demonstrate or invoke functionality in a standalone manner.
if __name__ == "__main__":
    # Usage: Replace with your actual file path as needed
    ## 3. os.path.join(Combine the base path with the filename
    path = os.path.join(base_path, "ai_voice.mp3")
    transcript = transcribe_audio(path)
    print(f"\n {transcript}")