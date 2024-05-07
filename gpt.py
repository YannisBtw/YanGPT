import requests
import logging

from creds import get_creds
from config import (LOGS, MAX_GPT_TOKENS, SYSTEM_PROMPT, LOG_FORMAT,
                    TOKENIZER_URL, GPT_URL)

logging.basicConfig(filename=LOGS, level=logging.ERROR, format=LOG_FORMAT,
                    filemode="w")


def count_gpt_tokens(messages):
    iam_token, folder_id = get_creds()
    headers = {
        'Authorization': f'Bearer {iam_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'modelUri': f"gpt://{folder_id}/yandexgpt-lite",
        "messages": messages
    }
    try:
        return len(
            requests.post(url=TOKENIZER_URL, json=data,
                          headers=headers).json()['tokens'])
    except Exception as e:
        logging.error(e)
        return 0


def ask_gpt(messages):
    iam_token, folder_id = get_creds()
    url = GPT_URL
    headers = {
        'Authorization': f'Bearer {iam_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'modelUri': f"gpt://{folder_id}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.7,
            "maxTokens": MAX_GPT_TOKENS
        },
        "messages": SYSTEM_PROMPT + messages
    }
    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code != 200:
            return False, f"Ошибка GPT: {response.status_code}", None

        answer = response.json()['result']['alternatives'][0]['message']['text']
        tokens_in_answer = count_gpt_tokens(
            [{'role': 'assistant', 'text': answer}])
        return True, answer, tokens_in_answer
    except Exception as e:
        logging.error(e)
        return False, "Ошибка при обращении к GPT", None
