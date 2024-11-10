import os
from dotenv import load_dotenv
load_dotenv()
user_api_key = os.getenv("API_KEY")
import speech_recognition as sr
from pathlib import Path
conversation_file_path = Path(__file__).parent / "conversation.txt"
from jarvis_STT import *

recognizer = sr.Recognizer()
microphone = sr.Microphone()

def main():
   clear_history()
   script_active = True

   with microphone as source:
      recognizer.pause_threshold = .5   
      print("\nAdjusting to ambient noise...")
      recognizer.adjust_for_ambient_noise(source, duration=5)
         
   while script_active:
      with microphone as source:
         script_active = standby(sr, source, recognizer, user_api_key)

# Clear the previous conversation in conversation.txt
def clear_history():
   conversation_txt = open(conversation_file_path, "a")
   conversation_txt.truncate(0)
   conversation_txt.close()

if __name__ == "__main__":
    main()