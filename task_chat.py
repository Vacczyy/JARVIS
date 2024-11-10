from openai import OpenAI
import datetime
from jarvis_app import conversation_file_path, user_api_key
from task_TTS import *

def inscribe(response):
   with open(conversation_file_path, "a") as conversation_txt:
      conversation_txt.write(f"({datetime.datetime.now()}) Response: {response}\n")

chat_instructions_short = """
You are an AI assistant that recieves an audio transcript and verbally communicates an answer.
Keep your response concise and under one sentence.
"""
def chat_short(transcription):
   print("Sending prompt.")
   conversation_txt = open(conversation_file_path, "r")
   client = OpenAI(api_key = user_api_key)
   response = client.chat.completions.create(
      model="gpt-3.5-turbo-0125",
      messages=[
      {
         "role": "system",
         "name": "JARVIS",
         "content": chat_instructions_short
      },
      {
         "role": "user",
         "content": transcription.strip()
      },
      {
         "role":"user",
         "name": "context",
         "content": conversation_txt.read()
      }
      ],
      temperature=0.25,
      max_tokens=500,
      top_p=1,
      frequency_penalty=0.1,
   )
   response, prompt_exit = response.choices[0].message.content, response.choices[0].finish_reason
   inscribe(response)

   print(f"\nPrompt: {transcription}\nResponse: {response}")
   text_to_speech(response)

chat_instructions_long = """
You are an AI assistant that recieves an audio transcript and verbally communicates an answer.
Keep your response under five sentences.
"""
def chat_long(transcription):
   conversation_txt = open(conversation_file_path, "r")
   client = OpenAI(api_key = user_api_key)
   response = client.chat.completions.create(
      model="gpt-3.5-turbo-0125",
      messages=[
      {
         "role": "system",
         "name": "JARVIS",
         "content": chat_instructions_long
      },
      {
         "role": "user",
         "content": transcription.strip()
      },
      {
         "role":"user",
         "name": "context",
         "content": conversation_txt.read()
      }
      ],
      temperature=0.25,
      max_tokens=1500,
      top_p=1,
      frequency_penalty=0.1,
   )
   response, prompt_exit = response.choices[0].message.content, response.choices[0].finish_reason
   inscribe(response)

   print(f"\nPrompt: {transcription}\nResponse: {response}")
   text_to_speech(response)

def chat(request_stack):
   def short():
      chat_short(request_stack[2])
   def long():
      chat_long(request_stack[2])

   function = locals().get(request_stack[1])
   function()
   
   return False