from .route_imports import *


accounts_bp = Blueprint('accounts', __name__, url_prefix='/account')


@accounts_bp.route('/@<username>', methods=['GET'])
@login_required
def get_account(current_user, username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template(
        'account-profile.html',
        current_user=current_user,
        user=user
    )


@accounts_bp.route('/@<username>', methods=['POST'])
@login_required
def edit_account(current_user, username):
    print(username, current_user)
    print(request.form)

    return {}


@accounts_bp.route('/@<username>/projects', methods=['GET'])
@login_required
def get_account_projects(current_user, username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template(
        'account-projects.html',
        current_user=current_user,
        user=user,
        projects=user.projects
    )


