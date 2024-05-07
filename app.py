from flask import redirect
from logging import basicConfig

from routes import *
from config import FLASK_PORT, FLASK_DEBUG_MODE, FLASK_HOST, LOG_FILE_PATH
from manage import app
from helpers import login_required

if LOG_FILE_PATH:
    basicConfig(filename=LOG_FILE_PATH)

app.register_blueprint(auth_bp)
app.register_blueprint(accounts_bp, url_prefix='/account')
app.register_blueprint(project_bp, url_prefil='/project')
app.register_blueprint(search_bp, url_prefil='/search')


@app.route('/')
@login_required
def index(current_user):
    return redirect('/search')


if __name__ == '__main__':
    app.run(
        host=FLASK_HOST,
        port=FLASK_PORT,
        debug=FLASK_DEBUG_MODE
    )
