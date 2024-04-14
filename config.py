from os import getenv
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

FLASK_PORT = getenv('FLASK_PORT')
FLASK_DEBUG_MODE = getenv('FLASK_DEBUG_MODE')
FLASK_APP_SECRET_KEY = getenv('FLASK_APP_SECRET_KEY')

DEFAULT_SESSION_TIME = timedelta(
    seconds=0,
    minutes=0,
    hours=1,
    days=0,
    weeks=0
)
LONG_SESSION_TIME = timedelta(
    seconds=0,
    minutes=0,
    hours=2,
    days=0,
    weeks=0
)  # Если пользователь при входе нажал "Запомнить меня"

POSTGRES_USERNAME = getenv('POSTGRES_USERNAME')
POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = getenv('POSTGRES_HOST')
POSTGRES_PORT = getenv('POSTGRES_PORT')
POSTGRES_DATABASE = getenv('POSTGRES_DATABASE')

SALT_FOR_USERS_COLOR_GENERATOR = "get"
SALT_FOR_PROJECTS_COLOR_GENERATOR = "pull"
