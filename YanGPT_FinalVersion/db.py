import sqlite3
import logging
from config import LOGS, LOG_FORMAT, DB_NAME, TABLE_NAME, COUNT_LAST_MSG

logging.basicConfig(filename=LOGS, level=logging.ERROR, format=LOG_FORMAT,
                    filemode="w")


def prepare_db():
    create_db()
    create_table(table_name=TABLE_NAME)


def create_db(database_name=DB_NAME):
    connection = sqlite3.connect(database_name, timeout=10)
    connection.close()


def execute_query(sql_query, data=None, db_path=DB_NAME):
    with sqlite3.connect(db_path, timeout=10) as connection:
        cursor = connection.cursor()
        if data:
            cursor.execute(sql_query, data)
        else:
            cursor.execute(sql_query)
        connection.commit()


def execute_selection_query(sql_query, data=None, db_path=DB_NAME):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    if data:
        cursor.execute(sql_query, data)
    else:
        cursor.execute(sql_query)
    rows = cursor.fetchall()
    connection.close()
    return rows


def create_table(table_name=TABLE_NAME):
    try:
        sql_query = f'''CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        message TEXT,
        role TEXT,
        total_gpt_tokens INTEGER,
        tts_symbols INTEGER,
        stt_blocks INTEGER)'''
        logging.info("DATABASE: База данных создана")
        execute_query(sql_query)
    except Exception as e:
        logging.error(e)
        return None


def add_message(user_id, full_message):
    try:
        message, role, total_gpt_tokens, tts_symbols, stt_blocks = full_message
        sql_query = (f"INSERT INTO {TABLE_NAME} (user_id, message, role, "
                     f"total_gpt_tokens, tts_symbols, stt_blocks)"
                     f" VALUES (?, ?, ?, ?, ?, ?)"), (user_id, message, role,
                                                      total_gpt_tokens,
                                                      tts_symbols, stt_blocks)
        execute_query(sql_query)
        logging.info(f"DATABASE: INSERT INTO messages "
                     f"VALUES ({user_id}, {message}, {role}, {total_gpt_tokens},"
                     f" {tts_symbols}, {stt_blocks})")
    except Exception as e:
        logging.error(e)
        return None


def count_users(user_id):
    try:
        sql_query = (f"SELECT COUNT(DISTINCT user_id) FROM {TABLE_NAME}"
                     f" WHERE user_id <> ?"), (user_id,)
        execute_selection_query(sql_query)
    except Exception as e:
        logging.error(e)
        return None


def select_n_last_messages(user_id, n_last_messages=COUNT_LAST_MSG):
    messages = []
    total_spent_tokens = 0
    try:
        sql_query = ('''SELECT message, role, total_gpt_tokens FROM messages
         WHERE user_id=? ORDER BY id DESC LIMIT ?''', (user_id, n_last_messages))
        data = execute_selection_query(sql_query)
        if data and data[0]:
            for message in reversed(data):
                messages.append({'text': message[0], 'role': message[1]})
                total_spent_tokens = max(total_spent_tokens, message[2])
        return messages, total_spent_tokens
    except Exception as e:
        logging.error(e)
        return messages, total_spent_tokens


def count_all_limits(user_id, limit_type):
    try:
        sql_query = (f'''SELECT SUM({limit_type}) FROM messages
         WHERE user_id=?''', (user_id,))
        data = execute_selection_query(sql_query)
        if data and data[0]:
            logging.info(f"DATABASE: У user_id={user_id}"
                         f" использовано {data[0]} {limit_type}")
            return data[0]
        else:
            return 0
    except Exception as e:
        logging.error(e)
        return 0

