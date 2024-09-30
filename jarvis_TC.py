from openai import OpenAI
import json
import os
import datetime
from importlib import import_module
from jarvis_app import conversation_file_path

task_list_file = open("task_list_file.txt", "r")
task_list = task_list_file.read().split()
for task in task_list:
    module = __import__(task)
    for attr in dir(module):
        if callable(getattr(module, attr)):
            globals()[attr] = getattr(module, attr)

with open('request_categories.json', 'r') as r:
    request_categories = json.load(r)

classification_intructions = """
You are an AI assistant that classifies a user request into categories. Only return one category, nothing else but the category, and every character lowercase.
These are the categories:
"""

for category, description in request_categories.items():
    classification_intructions += f'"{category}" {description}\n'

def sleep(request_stack):
   end_conversation = True
   return end_conversation

def terminate(request_stack):
   exit()

def unknown(request_stack):
   print("Request unknown.")

def text_classification(transcription, api_key, end_conversation):
   print("\nClassifying request.")
   conversation_txt = open(conversation_file_path, "a")
   client = OpenAI(api_key = api_key)
   response = client.chat.completions.create(
      model="gpt-3.5-turbo-0125",
      messages=[
      {
         "role": "system",
         "content": classification_intructions.strip()
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
   
   conversation_txt.write(f"({datetime.datetime.now()}) Request: {classification}\n")
   classification += f':{transcription}'
   request_stack = classification.rsplit(":")
   print(f"Request: {request_stack}")
   function = globals().get(request_stack[0])
   if function:
      end_conversation = function(request_stack)
   else:
      print(f"No request \"{request_stack[0]}\" found")
   return end_conversation