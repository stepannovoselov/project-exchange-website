from os import getenv
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

FLASK_PORT = getenv('FLASK_PORT')
FLASK_DEBUG_MODE = getenv('FLASK_DEBUG_MODE')
FLASK_APP_SECRET_KEY = getenv('FLASK_APP_SECRET_KEY')
FLASK_HOST = getenv('FLASK_HOST')

DEFAULT_SESSION_TIME = timedelta(
    seconds=int(getenv('DEFAULT_SESSION_TIME_SECONDS'))
)
LONG_SESSION_TIME = timedelta(
    seconds=int(getenv('LONG_SESSION_TIME_SECONDS'))
)

POSTGRES_USERNAME = getenv('POSTGRES_USERNAME')
POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = getenv('POSTGRES_HOST')
POSTGRES_PORT = getenv('POSTGRES_PORT')
POSTGRES_DATABASE = getenv('POSTGRES_DATABASE')

SALT_FOR_USERS_COLOR_GENERATOR = getenv('SALT_FOR_USERS_COLOR_GENERATOR')
SALT_FOR_PROJECTS_COLOR_GENERATOR = getenv('SALT_FOR_PROJECTS_COLOR_GENERATOR')

LOG_FILE_PATH = getenv('LOG_FILE_PATH')
