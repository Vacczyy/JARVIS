from dotenv import load_dotenv
load_dotenv()
import os
from jarvis_app import conversation_file_path
from jarvis_TC import text_classification
import time
import datetime

keyphrase = os.getenv("KEYPHRASE", "Jarvis")
timeout = float(os.getenv("TIMEOUT", 120))

def inscribe(transcription):
   conversation_txt = open(conversation_file_path, "a")
   conversation_txt.write(f"({datetime.datetime.now()}) Prompt: {transcription}\n")
   conversation_txt.close()

def standby(sr, source, recognizer, my_api_key):
   print("\nStandby initiated.")
   script_active = False
   end_conversation = False
   start_time = time.time()
   while time.time() - start_time < timeout:
      audio = recognizer.listen(source)
      try:
         recorded = recognizer.recognize_whisper_api(audio, api_key = my_api_key)
         if keyphrase in recorded:
            script_active = True
            break
      except sr.UnknownValueError:
         print("ERROR: Recognition failed.")
      except sr.RequestError as e:
         print(f"ERROR: Unable to request results- {e}")
   if script_active:
      while not end_conversation:
         end_conversation = listening(sr, source, recognizer, my_api_key, end_conversation)
   else:
      exit()
   return True

def listening(sr, source, recognizer, my_api_key, end_conversation):
   print("Listening.")
   start_time = time.time()
   while time.time() - start_time < timeout:
      audio = recognizer.listen(source)
      try:
         transcription = recognizer.recognize_whisper_api(audio, api_key=my_api_key)
         if transcription:
            inscribe(transcription)
            print("Audio transcribed.")
            end_conversation = text_classification(transcription, my_api_key, end_conversation)
            break
      except sr.UnknownValueError:
         print("ERROR: Transcription failed.")
      except sr.RequestError as e:
         print(f"ERROR: Unable to request results- {e}")
   return end_conversation