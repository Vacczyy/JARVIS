# JARVIS

JARVIS is a voice-activated chatbot written in Python that uses OpenAI API models GPT-3.5 Turbo, Whisper, and TTS. 

**You'll need an active API key and the latest version of Python 3 installed.**

## Installation

1. Start by cloning the project from GitHub:
```bash
git clone https://github.com/Vacczyy/JARVIS.git
cd DIRECTORY/TO/CLONE
```
2. Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # For Linux/macOS
# or
venv\Scripts\activate  # For Windows
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Add your API key to a .env file
```plaintext
API_KEY = "--paste here--"
```
## Usage

- In a terminal, run:
```bash
python3 DIRECTORY/TO/CLONE/jarvis_app.py
```
- An expected output should be somewhat like:
```plaintext
Adjusting to ambient noise...

Standby initiated.
Listening.
Audio transcribed.

Classifying request.
Request: [--classification--, --transcription--]
--Output--
```

## Request Categories

|Classification|Explanation|
|-|-|
|Chat|Basic text response to a question. Followed by either "short" or "long."|
|Standby|Ends the current conversation and puts JARVIS on standby. Allows for a new conversation to begin.|
|Sleep|Ends the conversation by killing the script.|
|None|The request does not match any categories and is disregarded.|

## Upcoming Features

- Web browser integration (search function, opening websites)
- Manual transcription trigger aside from voice activation
- GUI using Streamlit