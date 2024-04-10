from .route_imports import *

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET'])
@anonymous_required
def get_register_form():
    return render_template('register-form.html')


@auth_bp.route('/register', methods=['POST'])
@anonymous_required
@validate_request_data(schema=RegisterUserRequest)
@transaction
def register():
    hashed_password, salt, iterations = hash_password(request.form.get('password'))
    user = User(
        surname=request.form.get('surname'),
        name=request.form.get('name'),
        email=request.form.get('email'),
        username=request.form.get('username'),
        password=hashed_password,
        salt=salt,
        iterations=iterations,
    )
    db.session.add(user)

    return redirect('/login')


@auth_bp.route('/login', methods=['GET'])
@anonymous_required
def get_login_form():
    return render_template('login-form.html')


@auth_bp.route('/login', methods=['POST'])
@anonymous_required
@validate_request_data(schema=LoginUserRequest)
def login():
    username_of_email = request.form.get('username_or_email')
    if "@" in username_of_email:
        user = User.query.filter_by(email=username_of_email).first()
    else:
        user = User.query.filter_by(username=username_of_email).first()

    long_session = True if request.form.get('remember_me') == 'on' else False
    login_user(user.id, long_session)

    return redirect('/')


@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout(current_user):
    logout_user()

    return redirect('/')
