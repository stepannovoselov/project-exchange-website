from .route_imports import *
import json

project_bp = Blueprint('project', __name__, url_prefix='/project')


@project_bp.route('/create', methods=['GET'])
@login_required
def create_project_page(current_user):
    return render_template('create-project-form.html', current_user=current_user)


@project_bp.route('/create', methods=['POST'])
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
        tags=request.form.get('tags', None),
        vacancies=[vacancy for vacancy in json.loads(request.form.get('vacancies')) if all(vacancy[key] for key in vacancy.keys() if key != 'VacancyTags')],
        author=current_user
    )

    for user_id in request.form.get('teammates', []):
        try:
            user = User.query.filter_by(id=int(user_id)).first()
            if user:
                project.teammates.append(user)

        except:
            continue

    db.session.add(project)

    return jsonify({'status': 'ok', 'url': f'/account/@{current_user.username}'}), 200


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

    current_user_actions = UserAction.query.filter_by(user=current_user, project=project).all()
    if current_user_actions:
        current_user_actions = [act.action for act in current_user_actions]

    return render_template('project.html', current_user=current_user, project=project, current_user_actions=current_user_actions, actions_count=get_project_actions_count(project))


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


@project_bp.route('/ai/<ai_action>', methods=['GET'])
@login_required
def generate_project(current_user, ai_action):
    if ai_action == 'generate_project':
        return process_gpt_prompt(
            'Придумай интересный и полезный проект и заполни о нем следующие поля: «Название», «Тема», «Цель», «Описание», «Теги» (теги укажи через пробел).'
        )

    elif ai_action == 'generate_science':
        return process_gpt_prompt(
            'Придумай интересное реальное исследование и заполни о нем следующие поля: «Название», «Тема», «Цель», «Описание», «Теги» (теги укажи через пробел).'
        )

    elif ai_action == 'upgrade_text':
        edit_filed = request.values.get('edit')
        name = request.values.get('name')
        theme = request.values.get('theme')
        goal = request.values.get('goal')
        description = request.values.get('description')

        return process_gpt_prompt(
            f'Улучши текст для поля {edit_filed}, чтобы он звучал лучше и понятнее с полным сохранением смысла и длинны. Текст поля: {locals().get(edit_filed)}'
        )

    elif ai_action == 'fill_text':
        fill_filed = request.values.get('fill')
        name = request.values.get('name')
        theme = request.values.get('theme')
        goal = request.values.get('goal')
        description = request.values.get('description')

        return process_gpt_prompt(
            f'Заполни текст для поля {fill_filed} на основе других полей о проекте. Текст для поля должен быть понятным и объемным. Значения других полей: {name=}; {theme=}; {goal=}; {description=}'
        )

    else:
        return jsonify({
            'status': 'error'
        }), 404


@project_bp.route('/<int:project_id>/edit', methods=['GET'])
@login_required
def get_edit_project_form(current_user, project_id):
    project = Project.query.filter_by(id=project_id).first_or_404()

    return render_template('create-project-form.html', current_user=current_user, edit=True, project=project)


@project_bp.route('/<int:project_id>/edit', methods=['POST'])
@login_required
@validate_request_data(schema=CreateProjectUserRequest)
@transaction
def edit_project(current_user, project_id):
    project = Project.query.filter_by(id=project_id).first_or_404()

    if current_user.username == project.author.username:
        project.name = request.form.get('name')
        project.type = request.form.get('type')
        project.theme = request.form.get('theme', None)
        project.goal = request.form.get('goal', None)
        project.description = request.form.get('description', None)
        project.tags = request.form.get('tags', None)
        project.vacancies = [vacancy for vacancy in json.loads(request.form.get('vacancies')) if all(vacancy[key] for key in vacancy.keys() if key != 'VacancyTags')]

        project.teammates = []
        for user_id in request.form.get('teammates', []):
            try:
                user = User.query.filter_by(id=int(user_id)).first()
                if user:
                    project.teammates.append(user)

            except:
                continue

        return jsonify({'status': 'ok', 'url': f'/project/{project.id}'}), 200

