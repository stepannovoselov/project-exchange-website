from .route_imports import *

search_bp = Blueprint('search', __name__, url_prefix='/search')


@search_bp.route('/')
@search_bp.route('/projects')
@login_required
def search_projects(current_user):
    # params = [ key.replace('search_', '').replace('project_type_', '') for key, value in request.values.items() if
    # (value != 'off' and key != 'query') or key == 'query' ]
    #
    # q = Project.query
    #
    # for param in params:
    #     if param == 'query':

    projects = Project.query.all()
    return render_template('find-projects.html', current_user=current_user, projects=projects)


@search_bp.route('/users')
@login_required
def search_users(current_user):

    users = User.query.all()
    return render_template('find-users.html', current_user=current_user, users=users)
