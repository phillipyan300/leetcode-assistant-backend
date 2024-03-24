import requests
from dotenv import load_dotenv
import os

# API endpoint configuration
api_url = "https://transcribe.whisperapi.com"

load_dotenv()

APIKEY = os.getenv('WHISPER_API_KEY')

headers = {'Authorization': f'Bearer {APIKEY}'}

# Payload setup for API request
payload = {
    'file': {'file': open('./audioTests/badAnswer 2.1.m4a', 'rb')},
    'data': {
        "fileType": "m4a",  # Default is 'wav'.
        "diarization": "false",  # 'True' may slow down processing.
        #"numSpeakers": "2",  # Optional: Number of speakers for diarization. If blank, model will auto-detect.
        #"url": "URL_OF_STORED_AUDIO_FILE",  # Use either URL or file, not both.
        "initialPrompt": "",  # Optional: Teach model a phrase. May negatively impact results.
        "language": "en",  # Optional: Language of speech. If blank, model will auto-detect.
        "task": "transcribe",  # Use 'translate' to translate speech from language to English. Transcribe is default.
        "callbackURL": "",  # Optional: Callback URL for results to be sent.
    }
}

# Ensure the 'callbackURL' starts with 'https://' and does not include 'www.'
# The server calls the callback URL once the response is ready.

# Make the API request and print the response
response = requests.post(api_url, headers=headers, files=payload['file'], data=payload['data'])
print(response.text)

# Note: Omitting a parameter or setting it as an empty string "" allows for auto-detection.
# Keep in mind that auto-detected values may not always be accurate.


#Buy transcription time from this portal
#Generate an API key. You click the circular arrows above to generate a new key. We don't save the key, so keep it on you.
#Example API usage provided
#See API usage on this dashboard by day
#API usage rounded to nearest second per request, minimum 1 second per request
#Questions? Comments? Concerns? Email: info@whisperapi.com and we will respond