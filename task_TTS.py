from openai import OpenAI
from playsound import playsound
from jarvis_app import user_api_key

# Call OpenAI's TTS model and stream the returned audio
def text_to_speech(response):
   client = OpenAI(api_key = user_api_key)
   print("Formulating words.\n")
   tts_output = client.audio.speech.create(
       model="tts-1",
       voice="onyx",
       input=response,
       speed=1.5,
       response_format="wav"
   )
   tts_output.stream_to_file("../tts_audio.wav")
   playsound(str("../tts_audio.wav"))