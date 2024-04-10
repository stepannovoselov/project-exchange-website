from .route_imports import *

search_bp = Blueprint('search', __name__, url_prefix='/search')


@search_bp.route('/')
@search_bp.route('/projects')
def projects():
    return redirect('/')


@search_bp.route('/users')
def teammates():
    return redirect('/')
