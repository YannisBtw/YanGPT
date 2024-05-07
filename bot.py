import logging
import os

import telebot
from telebot.types import Message
from telebot.types import ReplyKeyboardMarkup

from creds import get_bot_token
from speechkit import text_to_speech, speech_to_text
from gpt import ask_gpt
from validators import (check_number_of_users, is_gpt_token_limit,
                        is_stt_block_limit, is_tts_symbol_limit)
from config import (LOGS, LOG_FORMAT, TESTER_ID, WELCOME_TEXT,
                    COUNT_LAST_MSG)
from db import prepare_db, add_message, select_n_last_messages

logging.basicConfig(filename=LOGS, level=logging.ERROR, format=LOG_FORMAT,
                    filemode="w")
bot = telebot.TeleBot(get_bot_token())
prepare_db()


def create_keyboard(buttons: list[str]) -> ReplyKeyboardMarkup:
    """
    Создает объект клавиатуры для бота по переданному списку строк.
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons)
    return keyboard


@bot.message_handler(commands=["start"])
def start(message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    bot.send_message(user_id, f"Привет, {user_name}! {WELCOME_TEXT}")


@bot.message_handler(commands=['debug'])
def debug(message: Message):
    try:
        user_id = message.chat.id
        if user_id == TESTER_ID:
            if os.path.exists('bot.log'):
                with open('bot.log', 'rb') as f:
                    bot.send_document(user_id, f)

            else:
                bot.send_message(user_id, "Файл с логами не найден")
        else:
            bot.send_message(user_id, "Команда не найдена")
    except Exception as e:
        logging.error(f"Произошла ошибка в функции debug: {e}")


@bot.message_handler(content_types=['voice'])
def handle_voice(message: Message):
    user_id = message.from_user.id
    try:
        status_check_users, error_message = check_number_of_users(user_id)
        if not status_check_users:
            bot.send_message(user_id, error_message)
            return

        stt_blocks, error_message = is_stt_block_limit(user_id,
                                                       message.voice.duration)
        if error_message:
            bot.send_message(user_id, error_message)
            return

        file_id = message.voice.file_id
        file_info = bot.get_file(file_id)
        file = bot.download_file(file_info.file_path)
        status_stt, stt_text = speech_to_text(file)
        if not status_stt:
            bot.send_message(user_id, stt_text)
            return

        add_message(user_id=user_id,
                    full_message=[stt_text, 'user', 0, 0, stt_blocks])

        last_messages, total_spent_tokens = select_n_last_messages(
            user_id, COUNT_LAST_MSG)
        total_gpt_tokens, error_message = is_gpt_token_limit(
            last_messages, total_spent_tokens)
        if error_message:
            bot.send_message(user_id, error_message)
            return

        status_gpt, answer_gpt, tokens_in_answer = ask_gpt(last_messages)
        if not status_gpt:
            bot.send_message(user_id, answer_gpt)
            return
        total_gpt_tokens += tokens_in_answer

        tts_symbols, error_message = is_tts_symbol_limit(user_id, answer_gpt)

        recording = [answer_gpt, 'assistant', total_gpt_tokens, tts_symbols, 0]
        add_message(user_id=user_id, full_message=recording)

        if error_message:
            bot.send_message(user_id, error_message)
            return

        status_tts, voice_response = text_to_speech(answer_gpt)
        if status_tts:
            bot.send_message(user_id, voice_response,
                             reply_to_message_id=message.id)
        else:
            bot.send_voice(user_id, answer_gpt, reply_to_message_id=message.id)
    except Exception as e:
        logging.error(e)
        bot.send_message(user_id, "Не получилось ответить."
                                  " Попробуй записать другое сообщение")


@bot.message_handler(content_types=['text'])
def handle_text(message: Message):
    try:
        user_id = message.from_user.id

        status_check_users, error_message = check_number_of_users(user_id)
        if not status_check_users:
            bot.send_message(user_id, error_message)
            return

        full_user_message = [message.text, 'user', 0, 0, 0]
        add_message(user_id=user_id, full_message=full_user_message)

        last_messages, total_spent_tokens = select_n_last_messages(
            user_id, COUNT_LAST_MSG)
        total_gpt_tokens, error_message = is_gpt_token_limit(
            last_messages, total_spent_tokens)
        if error_message:
            bot.send_message(user_id, error_message)
            return

        status_gpt, answer_gpt, tokens_in_answer = ask_gpt(last_messages)
        if not status_gpt:
            bot.send_message(user_id, answer_gpt)
            return

        total_gpt_tokens += tokens_in_answer

        full_gpt_message = [answer_gpt, 'assistant', total_gpt_tokens, 0, 0]
        add_message(user_id=user_id, full_message=full_gpt_message)

        bot.send_message(user_id, answer_gpt, reply_to_message_id=message.id)

    except Exception as e:
        logging.error(e)
        bot.send_message(message.from_user.id,
                         "Не получилось ответить. Попробуй написать"
                         " другое сообщение")


@bot.message_handler(func=lambda: True)
def handler(message):
    bot.send_message(message.from_user.id, "Отправь мне голосовое или"
                                           " текстовое сообщение и бот ответит")
