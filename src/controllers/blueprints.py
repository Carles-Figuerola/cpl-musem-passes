from flask import request, current_app, Blueprint

index_bp = Blueprint('index', __name__)

@index_bp.route('/health')
def healthcheck():
    return '200 OK'


@index_bp.route('/api/<user>')
def api_status_for_user(user):
    logger = current_app.config['logger']
    diff_finder = current_app.config['diff_finder']
    config_users = current_app.config['user_keys']

    if user in config_users:
        logger.info(f'Matched user {user} in the config')
        availability = diff_finder.diff_and_return_for_user(user)

    return availability


@index_bp.route('/api/<user>')
def index():
    return '200 OK'
