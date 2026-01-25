from gtts import gTTS
import os
from dotenv import load_dotenv, find_dotenv
# 1. LOAD CONFIGURATION
# find_dotenv() must have () to work correctly
# MySQL credentials
load_dotenv(find_dotenv())
# Fetching all components from .env
# 2. Get the base path from the environment variable
base_path = os.getenv("MY_PROJECT_PATH")

# 1. The text you want the AI to say
my_text = "When a regular driver reads the manual (imports the file), they only want the instructions; they don't want the car to crash test. The crash test only happens at the factory (when the file is run directly"

# This sends the text to Google's neural speech models
tts = gTTS(text=my_text, lang='en', slow=False)

# 3. Save the result as an audio file

audio_file = os.path.join(base_path, "ai_voice.mp3")
tts.save(audio_file)

# 4. Play the file (Windows command)
print("Playing audio...")
os.system(f"start {audio_file}")