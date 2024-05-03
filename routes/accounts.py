from .route_imports import *

accounts_bp = Blueprint('accounts', __name__, url_prefix='/account')


@accounts_bp.route('/', methods=['GET'])
@accounts_bp.route('/@<got_username>', methods=['GET'])
@login_required
def get_account(current_user, got_username=None):
    username = got_username
    if got_username is None:
        username = current_user.username

    user = User.query.filter_by(username=username).first_or_404()

    if username == current_user.username and got_username is not None:
        return redirect('/account')

    return render_template(
        'account-profile.html',
        current_user=current_user,
        user=user
    )


@accounts_bp.route('/view', methods=['GET'])
@login_required
def view_user_account_from_side(current_user):
    user = User.query.filter_by(username=current_user.username).first_or_404()

    return render_template(
        'account-profile.html',
        current_user={'name': current_user.name, 'surname': current_user.surname},
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

            if key in ["vk_link", "telegram_link", "github_link", "email_link", "education", "skills", "hobbies",
                       'tags']:
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


@accounts_bp.route('/password', methods=['POST'])
@login_required
@validate_request_data(schema=ChangePasswordUserRequest)
@transaction
def change_password(current_user):
    current_user.password, current_user.salt, current_user.iterations = hash_password(request.form['newPassword'])
    return jsonify({'status': 'ok'}), 200


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


@accounts_bp.route('/users', methods=['GET'])
@login_required
def get_usernames_and_names(current_user):
    query = request.values.get('query', None)
    except_me = request.values.get('except_me', False)

    if query:
        if not except_me:
            users = User.query.filter(
                (func.lower(User.username).like(f'%{query.lower()}%')) |
                (func.lower(User.name).like(f'%{query.lower()}%')) |
                (func.lower(User.surname).like(f'%{query.lower()}%'))
            ).all()

        else:
            users = User.query.filter(
                    and_(func.lower(User.username) != current_user.username.lower()),
                    ((func.lower(User.username).like(f'%{query.lower()}%')) |
                     (func.lower(User.name).like(f'%{query.lower()}%')) |
                     (func.lower(User.surname).like(f'%{query.lower()}%')))
            ).all()

    else:
        if not except_me:
            users = User.query.all()
        else:
            users = User.query.filter(func.lower(User.username) != current_user.username.lower()).all()

    return jsonify([{
        'id': user.id,
        'surname': user.surname,
        'name': user.name,
        'username': user.username
    } for user in users])
