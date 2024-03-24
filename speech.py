import requests
from dotenv import load_dotenv
import os

def transcribe(fileName: str):

    # API endpoint configuration
    api_url = "https://transcribe.whisperapi.com"

    load_dotenv()

    APIKEY = os.getenv('WHISPER_API_KEY')

    headers = {'Authorization': f'Bearer {APIKEY}'}

    # Payload setup for API request
    payload = {
        'file': {'file': open(f'./audioTests/{fileName}', 'rb')},
        'data': {
            "fileType": "webm",  # Default is 'wav'.
            "diarization": "false",  # 'True' may slow down processing.
            #"numSpeakers": "2",  # Optional: Number of speakers for diarization. If blank, model will auto-detect.
            #"url": "URL_OF_STORED_AUDIO_FILE",  # Use either URL or file, not both.
            "initialPrompt": "",  # Optional: Teach model a phrase. May negatively impact results.
            "language": "en",  # Optional: Language of speech. If blank, model will auto-detect.
            "task": "transcribe",  # Use 'translate' to translate speech from language to English. Transcribe is default.
            "callbackURL": "",  # Optional: Callback URL for results to be sent.
        }
    }
    # Make the API request and print the response
    response = requests.post(api_url, headers=headers, files=payload['file'], data=payload['data'])
    return str(response.text)