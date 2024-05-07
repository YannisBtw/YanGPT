MAX_USERS = 3

MAX_GPT_TOKENS = 120

COUNT_LAST_MSG = 4

MAX_USER_STT_BLOCKS = 10

MAX_USER_TTS_SYMBOLS = 5000

MAX_USER_GPT_TOKENS = 2000

TESTER_ID = 1313337053

HOME_DIR = '/home/student/YanGPT'

LOGS = f'{HOME_DIR}/logs.txt'

DB_NAME = f'{HOME_DIR}/messages.db'

TABLE_NAME = "messages"

SYSTEM_PROMPT = [{'role': 'system',
                  'text': 'Ты вежливый и умный помощник, давай пользователю '
                          'максимально понятный и полный ответ, а также будь '
                          'к нему добр, старайся вести себя как человек.'}]

TOKENIZER_URL =\
    "https://llm.api.cloud.yandex.net/foundationModels/v1/tokenizeCompletion"

GPT_URL =\
    "https://llm.api.cloud.yandex.net/foundationModels/v1/tokenizeCompletion"

URL_SPEECHKIT_TTS = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'

URL_SPEECHKIT_STT = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize"

URL_CREDS =("http://169.254.169.254/computeMetadata/v1/instance"
            "/service-accounts/default/token")

LANG = "ru-RU"

VOICE = 'madirus'

SPEED = 0.7

WELCOME_TEXT = ("Привет! Отправь текстовое сообщение с каким-то вопросом или "
                "заданием и получи на него текстовый ответ или отправь "
                "голосовое сообщение, чтобы получить ответ в аудиоформате.")

LOG_FORMAT = ("%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %("
              "message)s")

IAM_TOKEN_PATH = f'{HOME_DIR}/creds/iam_token.txt'

FOLDER_ID_PATH = f'{HOME_DIR}/creds/folder_id.txt'

BOT_TOKEN_PATH = f'{HOME_DIR}/creds/bot_token.txt'
