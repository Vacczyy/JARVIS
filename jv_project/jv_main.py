import os
import sys
import json
import time

from dotenv import load_dotenv
load_dotenv()
jarvis_api_key = os.getenv("API_KEY")

from openai import OpenAI
import speech_recognition as sr
from playsound import playsound

# Create and open files
history = open('./history.txt', 'a')

history = open('history.txt', 'r+')
with open('./request_categories.json', 'r') as file:
    request_categories = json.load(file)
tts_audio = 'tts_audio.wav'

# Set up recognizer module
recognizer = sr.Recognizer()
microphone = sr.Microphone()
keyphrase = os.getenv("KEYPHRASE", "Jarvis")
jv_auto_sleep = os.getenv("AUTO_SLEEP_TIME", 60)       

# GPT Instructions
classification_intructions = """
You are an AI assistant that classifies a user request into categories. Only return one category, nothing else but the category, and every character lowercase.
These are the categories:
"""
for category, description in request_categories.items():
    classification_intructions += f'"{category}" {description}\n'

chat_instructions_short = """
You are an AI assistant that recieves an audio transcript and verbally communicates an answer.
Keep your response concise and under one sentence.
"""

chat_instructions_long = """
You are an AI assistant that recieves an audio transcript and verbally communicates an answer.
Keep your response around five sentences unless instructed otherwise.
"""

# History.txt functions
def inscribe(type, content):
   history.write(f"{type}: {content}\n")

def clear_history():
   history.truncate(0)

with microphone as source:
   recognizer.pause_threshold = 1
   print("\nADJUSTING TO AMBIENT NOISE")
   recognizer.adjust_for_ambient_noise(source, duration=5)

def main():
   clear_history()
   with microphone as source:
      inactive()

def inactive():
   awake = True
   conversation = False
   print("\nINACTIVE")
   while awake:
      try:
         with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=jv_auto_sleep)
            recorded = recognizer.recognize_whisper_api(audio, api_key=jarvis_api_key)
         if keyphrase.lower() in recorded.lower():
            conversation = True
            while conversation:
               awake, conversation = listening(awake, conversation)
               if awake and not conversation:
                  print("\nINACTIVE")
      except sr.UnknownValueError:
         print("ERR: Recognition failed.")
      except sr.RequestError as e:
         print(f"ERR: Whisper API error - {e}")
         sys.exit()
      except sr.WaitTimeoutError:
         print("EXIT: Auto sleep")
         sys.exit()

def listening(awake, conversation):
   print("\nLISTENING")
   transcription = None
   try:
      audio = recognizer.listen(source, timeout=10)
      transcription = recognizer.recognize_whisper_api(audio, api_key=jarvis_api_key)
      if transcription:
         inscribe("INPUT", transcription)
         print(f"INPUT: {transcription}")
         return classify(transcription, awake, conversation)
   except sr.UnknownValueError:
      print("ERR: Transcription failed.")
   except sr.RequestError as e:
      print(f"ERR: Whisper API error - {e}")
   except sr.WaitTimeoutError:
      print("TIMED OUT WHILE LISTENING")
   return awake, conversation

def classify(transcription, awake, conversation):
   print("\nCLASSIFYING REQUEST...")

   client = OpenAI(api_key = jarvis_api_key)
   response = client.chat.completions.create(
      model="gpt-3.5-turbo-0125",
      messages=[
      {
         "role": "system",
         "content": classification_intructions
      },
      {
         "role": "user",
         "content": transcription.strip()
      }
      ],
      temperature=0,
      max_tokens=20,
      top_p=0.75,
   )
   classification = response.choices[0].message.content.strip()
   
   classification += f':{transcription}'
   request_stack = classification.rsplit(":")
   function = globals().get(request_stack[0])

   inscribe("CLASSIFICATION", classification)
   print(f"CLASSIFICATION: {request_stack}")
   
   if function:
      awake, conversation = function(request_stack)
   else:
      print(f"REQUEST \"{request_stack[0]}\" UNKNOWN")
   return awake, conversation

# Tasks
def chat_short(transcription):
   client = OpenAI(api_key=jarvis_api_key)
   print("\nTHINKING...")

   chat_out = client.chat.completions.create(
      model="gpt-3.5-turbo-0125",
     messages = [
        {"role": "user", "content": str(transcription)}
      ],
      temperature=0.25,
      max_tokens=500,
      top_p=1,
      frequency_penalty=0.1,
   ) 
   chat_out = chat_out.choices[0].message.content.strip()

   inscribe("RESPONSE", chat_out)
   print(f"RESPONSE: {chat_out}")
   tts(chat_out)
   return True, True

def chat_long(transcription):
   client = OpenAI(api_key=jarvis_api_key)
   print("\nTHINKING...")

   chat_out = client.chat.completions.create(
      model="gpt-3.5-turbo-0125",
      messages = [
         {"role": "user", "content": str(transcription)}
      ],
      temperature=0.25,
      max_tokens=1500,
      top_p=1,
      frequency_penalty=0.1,
   )
   chat_out = chat_out.choices[0].message.content.strip()

   inscribe("RESPONSE", chat_out)
   print(f"RESPONSE: {chat_out}")
   tts(chat_out)
   return True, True

def tts(chat_out):
   client = OpenAI(api_key = jarvis_api_key)
   print("\nFORMULATING SPEECH...")

   with client.audio.speech.with_streaming_response.create(
       model="tts-1",
       voice="onyx",
       input=chat_out,
       response_format="wav"
   ) as tts_out:
      tts_out.stream_to_file(tts_audio)

   print("SPEAKING")
   playsound(tts_audio)

def standby(request_stack):
   return True, False

def sleep(request_stack):
   return False, False

def unknown(request_stack):
   print(f"REQUEST \"{request_stack[0]}\" UNKNOWN")
   return True, True

if __name__ == "__main__":
   main()