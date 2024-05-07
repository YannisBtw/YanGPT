import requests

from creds import get_creds
from config import URL_SPEECHKIT_TTS, URL_SPEECHKIT_STT, LANG, VOICE, SPEED


def text_to_speech(text):
    iam_token, folder_id = get_creds()

    headers = {"Authorization": f"Bearer {iam_token}", }

    data = {
        "text": text,
        "lang": LANG,
        'voice': VOICE,
        'speed': SPEED,
        'folderId': folder_id,
    }

    response = requests.post(URL_SPEECHKIT_TTS, headers=headers, data=data)

    if response.status_code == 200:
        return True, response.content
    else:
        return False, "При запросе в SpeechKit возникла ошибка"


def speech_to_text(data):
    iam_token, folder_id = get_creds()

    params = "&".join([
        "topic=general",
        f"folderId={folder_id}",
        "lang=ru-RU"
    ])

    headers = {'Authorization': f'Bearer {iam_token}',}

    response = requests.post(f"{URL_SPEECHKIT_STT}?{params}",
                             headers=headers, data=data
                             )

    decoded_data = response.json()
    if decoded_data.get("error_code") is None:
        return True, decoded_data.get("result")
    else:
        return False, "При запросе в SpeechKit возникла ошибка"
