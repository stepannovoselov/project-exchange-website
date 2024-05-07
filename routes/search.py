from .route_imports import *

search_bp = Blueprint('search', __name__, url_prefix='/search')


@search_bp.route('/', methods=['GET'])
@search_bp.route('/projects', methods=['GET'])
@login_required
def search_projects(current_user):
    params = [key for key, param in request.values.items() if param == 'on' or key != 'query']

    type_filters = []
    search_by_filters = []
    query = request.values.get('query')
    for param in params:
        if param.startswith('project_type_'):
            project_type = param[13:]
            if project_type == 'project':
                type_filters.append('Проект')
            elif project_type == 'science':
                type_filters.append('Исследование')
            elif project_type == 'idea':
                type_filters.append('Идея')

        elif param.startswith('search_'):
            search_by = param[7:]
            search_by_filters.append(search_by)

    q = Project.query
    if type_filters:
        q = q.filter(Project.type.in_(type_filters))

    if query is not None and query.strip() != '':
        or_conditions = []
        for column_name in search_by_filters:
            column = getattr(Project, column_name, None)
            if column is not None:
                if 'author' in str(column):
                    if query.startswith('@'):
                        query = query[1:]
                    or_conditions.append(func.lower(User.name).contains(f'%{query.lower()}%'))
                    or_conditions.append(func.lower(User.surname).contains(f'%{query.lower()}%'))
                    or_conditions.append(func.lower(User.username).contains(f'%{query.lower()}%'))
                else:
                    or_conditions.append(func.lower(column).contains(f'%{query.lower()}%'))
        if or_conditions:
            q = q.filter(or_(*or_conditions))

    projects = q.all()
    projects.sort(key=lambda e: len([i for i in e.actions if i.action == 'mark' or i.action == 'like']), reverse=True)

    return render_template('find-projects.html', current_user=current_user, projects=projects, values=request.values, actions_count=get_project_actions_count(q.all(), one_project=False))


@search_bp.route('/users', methods=['GET'])
@login_required
def search_users(current_user):
    params = [key for key, param in request.values.items() if param == 'on' or key != 'query']

    search_by_filters = []
    query = request.values.get('query')
    for param in params:
        if param.startswith('users_search_by_'):
            search_by = param[16:]

            if search_by == 'name_and_surname':
                search_by_filters.append('name')
                search_by_filters.append('surname')
            else:
                search_by_filters.append(search_by)

    q = User.query.outerjoin(User.projects).group_by(User.id).order_by(func.count(Project.id).desc())
    if query is not None and query.strip() != '':
        or_conditions = []
        for column_name in search_by_filters:
            column = getattr(User, column_name, None)
            if column is not None:
                or_conditions.append(func.lower(column).contains(f'%{query.lower()}%'))
            elif column_name in ['education', 'skills', 'hobbies', 'tags']:
                or_conditions.append(func.lower(func.json_extract_path_text(User.about, column_name)).contains(f'{query.lower()}'))

        if or_conditions:
            q = q.filter(or_(*or_conditions))

    return render_template('find-users.html', current_user=current_user, users=q.all(), values=request.values)
