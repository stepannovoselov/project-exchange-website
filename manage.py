from flask import Flask
from flask_migrate import Migrate

from config import POSTGRES_USERNAME, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DATABASE, FLASK_APP_SECRET_KEY
from models import db


app = Flask(__name__)
app.secret_key = FLASK_APP_SECRET_KEY


db_string = "postgresql://{}:{}@{}:{}/{}".format(
    POSTGRES_USERNAME,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DATABASE
)
app.config['SQLALCHEMY_DATABASE_URI'] = db_string


db.init_app(app)
migrations = Migrate(app, db)

