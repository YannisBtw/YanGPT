import requests
import logging

from config import (LOGS, MAX_GPT_TOKENS, SYSTEM_PROMPT, IAM_TOKEN, FOLDER_ID,
                    LOG_FORMAT, TOKENIZER_URL, GPT_URL)

logging.basicConfig(filename=LOGS, level=logging.ERROR, format=LOG_FORMAT,
                    filemode="w")


def count_gpt_tokens(messages):
    url = TOKENIZER_URL
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'modelUri': f"gpt://{FOLDER_ID}/yandexgpt-lite",
        "messages": messages
    }
    try:
        return len(
            requests.post(url=url, json=data, headers=headers).json()['tokens'])
    except Exception as e:
        logging.error(e)
        return 0


def ask_gpt(messages):
    url = GPT_URL
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'modelUri': f"gpt://{FOLDER_ID}/yandexgpt-lite",
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
