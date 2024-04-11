from .route_imports import *

project_bp = Blueprint('project', __name__, url_prefix='/project')


@project_bp.route('/create', methods=['get'])
@login_required
def create_project_page(current_user):
    return render_template('create-project-form.html', current_user=current_user)


@project_bp.route('/create', methods=['post'])
@login_required
@validate_request_data(schema=CreateProjectUserRequest)
@transaction
def create_project(current_user):
    project = Project(
        name=request.form.get('name'),
        type=request.form.get('type'),
        theme=request.form.get('theme', None),
        goal=request.form.get('goal', None),
        description=request.form.get('description', None),
        author=current_user
    )
    db.session.add(project)
    return redirect(f'/account/@{current_user.username}')


@project_bp.route('/<int:project_id>')
def show_project(project_id):
    projectdata = cursor.execute('''SELECT * FROM projects WHERE id = ?''', (project_id,)).fetchone()
    print(projectdata)
    return render_template('project.html', projectdata=projectdata)
