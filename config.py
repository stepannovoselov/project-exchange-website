from os import getenv
from dotenv import load_dotenv
from datetime import timedelta


load_dotenv(dotenv_path='.env')

FLASK_PORT = getenv('FLASK_PORT')
FLASK_DEBUG_MODE = getenv('FLASK_DEBUG_MODE')
FLASK_APP_SECRET_KEY = getenv('FLASK_APP_SECRET_KEY')

DEFAULT_SESSION_TIME = timedelta(
    hours=1
)
LONG_SESSION_TIME = timedelta(
    hours=2
)  # Если пользователь при входе нажал "Запомнить меня"

POSTGRES_USERNAME = getenv('POSTGRES_USERNAME')
POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = getenv('POSTGRES_HOST')
POSTGRES_PORT = getenv('POSTGRES_PORT')
POSTGRES_DATABASE = getenv('POSTGRES_DATABASE')
