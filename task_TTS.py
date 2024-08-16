from pathlib import Path
from openai import OpenAI
from playsound import playsound
from jarvis_app import my_api_key
import os

# Call OpenAI's TTS model and stream the returned audio
def text_to_speech(response):
   client = OpenAI(api_key = my_api_key)
   tts_audio_file = Path(__file__).parent / "tts_audio.mp3"
   print("Formulating words.")
   tts_output = client.audio.speech.create(
       model="tts-1",
       voice="onyx",
       input=response,
       speed=1.1,
   )
   tts_output.stream_to_file(tts_audio_file)
   print("\nSpeaking.")
   playsound(tts_audio_file)