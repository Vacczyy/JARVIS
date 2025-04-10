# JARVIS

JARVIS is a voice-activated chatbot written in Python that uses OpenAI models GPT-3.5 Turbo, Whisper, and TTS. 
**You'll need an active API key and the latest version of Python 3 installed.**

## Installation

1. Clone the project from GitHub:
```bash
git clone https://github.com/Vacczyy/JARVIS.git
cd --DIRECTORY/TO/CLONE--
```
2. Create a Virtual Environment
3. Install dependencies from requirements.txt
4. Add your API key to a .env file
```plaintext
API_KEY = "--(paste here)--"
KEYPHRASE = "--(Optional)--"
```
## Usage

- In a terminal, run jarvis_app.py
- When you see 'INACTIVE,' Jarvis is in a state where it will wait for the keyphrase before paying attention.
- Once Jarvis is listening, say your request into the microphone.
- The expected output should be somewhat like:
```plaintext
ADJUSTING TO AMBIENT NOISE

INACTIVE

LISTENING

INPUT: ----

CLASSIFYING REQUEST...
CLASSIFICATION: [--classification--, --transcription--]

THINKING...
RESPONSE: ----

FORMULATING SPEECH...
SPEAKING
```

## Request Categories

|Classification|Explanation|
|-|-|
|Chat|A short or long response to a question. Defaults to short unless asked otherwise.|
|Standby|Ends the current conversation but doesn't kill the program.|
|Sleep|Kills the script.|
|Unknown|The request does not match any categories.|

## Upcoming Features

- Interruptions through multithreading
- Manual trigger
- Streamlit UI