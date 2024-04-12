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
    return redirect(f'/account/@{current_user.username}/projects')


@project_bp.route('/<int:project_id>/delete', methods=['POST'])
@login_required
@transaction
def delete_project(current_user, project_id):
    if project_id in [p.id for p in current_user.projects]:
        project = Project.query.filter_by(id=project_id).first_or_404()
        db.session.delete(project)

        return jsonify({'status': 'ok'}), 200
    else:
        return jsonify({'status': 'error'}), 403
