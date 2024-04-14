from flask import redirect

from routes import *
from config import FLASK_PORT, FLASK_DEBUG_MODE
from manage import app
from helpers import login_required


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
        port=FLASK_PORT,
        debug=FLASK_DEBUG_MODE
    )
