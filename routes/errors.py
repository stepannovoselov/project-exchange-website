from route_imports import *

error_bp = Blueprint('error', __name__)


@error_bp.errorhandler(404)
def not_found_error(error_text):
    pass
