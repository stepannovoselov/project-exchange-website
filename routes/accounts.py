from .route_imports import *


accounts_bp = Blueprint('accounts', __name__, url_prefix='/account')


@accounts_bp.route('/', methods=['GET'])
@accounts_bp.route('/@<username>', methods=['GET'])
@login_required
def get_account(current_user, username=None):
    if username is None:
        username = current_user.username
    user = User.query.filter_by(username=username).first_or_404()

    return render_template(
        'account-profile.html',
        current_user=current_user,
        user=user
    )


@accounts_bp.route('/', methods=['POST'])
@accounts_bp.route('/@<username>', methods=['POST'])
@login_required
@validate_request_data(schema=EditProfileUserRequest)
@transaction
def edit_account(current_user, username=None):
    if username is None:
        username = current_user.username

    if current_user.username == username:
        for key, value in request.form.items():
            if key in ['name', 'surname']:
                value = value.capitalize()
                
            if key in ["vk_link", "telegram_link", "github_link", "email_link", "education", "skills", "hobbies", 'tags']:
                if not current_user.about:
                    current_user.about = {}

                if value.strip() != '' and value.strip() != 'Не указано':
                    current_user.about[key] = value.strip()
                else:
                    current_user.about[key] = ''

                flag_modified(current_user, "about")
                set_attribute(current_user, "about", current_user.about)

            else:
                setattr(current_user, key, value.strip())

        return jsonify({'status': 'ok', 'current_values': current_user.json_editable_except_password()}), 200

    return jsonify({'status': 'error', 'errors': {''}}), 404


@accounts_bp.route('/@<username>/password', methods=['POST'])
@login_required
@validate_request_data(schema=ChangePasswordUserRequest)
@transaction
def change_password(current_user, username):
    if current_user.username == username:
        current_user.password, current_user.salt, current_user.iterations = hash_password(request.form['newPassword'])
        return jsonify({'status': 'ok'}), 200

    return jsonify({'status': 'error'}), 403


@accounts_bp.route('/@<username>/projects', methods=['GET'])
@login_required
def get_account_projects(current_user, username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template(
        'account-projects.html',
        current_user=current_user,
        user=user,
        projects=sorted(user.projects, key=attrgetter('public_date'), reverse=True)
    )


@accounts_bp.route('/@<username>/bookmarks', methods=['GET'])
@login_required
def get_account_bookmarks(current_user, username):
    if current_user.username == username:
        mark_actions = UserAction.query.filter_by(user=current_user, action='mark').all()
        bookmarks = []
        for action in mark_actions:
            bookmarks.append(
                Project.query.filter_by(id=action.project.id).first()
            )
        return render_template('account-bookmarks.html', current_user=current_user, bookmarks=bookmarks)

    return redirect(f'/account/@{username}')

