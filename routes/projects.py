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


@project_bp.route('/<int:project_id>', methods=['GET'])
@login_required
def get_project(current_user, project_id):
    project = Project.query.filter_by(id=project_id).first_or_404()

    actions = UserAction.query.filter_by(user=current_user, project=project).all()
    if actions:
        actions = [act.action for act in actions]

    return render_template('project.html', current_user=current_user, project=project, actions=actions)


@project_bp.route('/<int:project_id>/<action>', methods=['POST'])
@login_required
@transaction
def make_project_action(current_user, project_id, action):
    if action in ['mark', 'like', 'dislike']:
        project = Project.query.filter_by(id=project_id).first_or_404()

        action_ = UserAction.query.filter_by(user=current_user, project=project, action=action).first()

        opposite_action = UserAction.query.filter_by(user=current_user, project=project, action='like' if action == 'dislike' else 'dislike').first()
        if opposite_action:
            db.session.delete(opposite_action)

        if not action_:
            if action == 'like' or action == 'dislike':
                action_ = UserAction(user=current_user, project=project, action=action)
                db.session.add(action_)

            elif action == 'mark':
                if not UserAction.query.filter_by(user=current_user, project=project, action='mark').first():
                    action_ = UserAction(
                        user=current_user,
                        project=project,
                        action=action
                    )
                    db.session.add(action_)
                else:
                    db.session.delete(action_)
            else:
                return jsonify({'status': 'error'}), 403
        else:
            db.session.delete(action_)

        return jsonify({'status': 'ok'}), 200

    return jsonify({'status': 'error'}), 404
