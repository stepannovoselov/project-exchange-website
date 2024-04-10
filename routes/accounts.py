from .route_imports import *


accounts_bp = Blueprint('accounts', __name__, url_prefix='/account')


@accounts_bp.route('/@<username>', methods=['GET'])
@login_required
def account(current_user, username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template(
        'account.html',
        current_user=current_user,
        user=user,
        projects=user.projects
    )
