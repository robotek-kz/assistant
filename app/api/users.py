from apifairy.decorators import other_responses
from flask import Blueprint, abort, request
from apifairy import authenticate, body, response

from api import db
from api.models import User, GameSketch, TemplateSketch, ProjectGameSketch, FileGameSketch, TemplateFileSketch, TemplateProjectSketch, \
    LinesUserLink, ApplicationUserLink, EpisodeUserLink
from api.schemas import UserSchema, UpdateUserSchema, EmptySchema, EpisodeSchema, EpisodeUserLinkSchema, LinesUserLinkSchema, UpdateLinesUserLinkSchema
from api.auth import token_auth
from api.decorators import paginated_response
from sqlalchemy.orm import joinedload
import pdb

users = Blueprint('users', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)
episodes_user_schema = EpisodeUserLinkSchema(many=True)
update_user_schema = UpdateUserSchema(partial=True)
line_user_schema = LinesUserLinkSchema()
lines_user_schema = LinesUserLinkSchema(many=True)
update_lines_user_schema = UpdateLinesUserLinkSchema()


@users.route('/users', methods=['POST'])
@body(user_schema)
@response(user_schema, 201)
def new(args):
    """Register a new user"""
    user = User(**args)
    template_project_sketches = db.session.scalars(
        'select * from template_project_sketches').all()
    for t_project in template_project_sketches:
        template_project_sketch = db.session.get(
            TemplateProjectSketch, t_project)
        # pdb.set_trace()
        project_game_sketch = ProjectGameSketch(
            user=user, name=template_project_sketch.__dict__.get('name'))
        db.session.add(project_game_sketch)
        # db.session.commit()
        for t_file in template_project_sketch.template_file_sketches:
            file_game_sketch = FileGameSketch(
                user=user, name=t_file.name, code='', project_game_sketches=project_game_sketch)
            db.session.add(file_game_sketch)
            # db.session.commit()
            for t_sketch in t_file.template_sketches:
                t_sketch.__dict__.pop("_sa_instance_state")
                t_sketch.__dict__.pop("id")
                t_sketch.__dict__.pop("template_file_sketch_id")
                game_sketch = GameSketch(
                    user=user, file_game_sketches=file_game_sketch, **t_sketch.__dict__)
                db.session.add(game_sketch)
    db.session.add(user)
    db.session.commit()
    return user


@users.route('/users', methods=['GET'])
@authenticate(token_auth)
@response(users_schema, 201)
def user_all():
    """Retrieve all users"""
    return db.session.scalars(User.select()).all()


@users.route('/users/<int:id>', methods=['GET'])
@authenticate(token_auth)
@response(user_schema)
@other_responses({404: 'User not found'})
def get(id):
    """Retrieve a user by id"""
    return db.session.get(User, id) or abort(404)


@users.route('/users/<nickname>', methods=['GET'])
@authenticate(token_auth)
@response(user_schema)
@other_responses({404: 'User not found'})
def get_by_nickname(nickname):
    """Retrieve a user by nickname"""
    return db.session.scalar(User.select().filter_by(nickname=nickname)) or \
        abort(404)


@users.route('/me', methods=['GET'])
@authenticate(token_auth)
@response(user_schema)
def me():
    """Retrieve the authenticated user"""
    return token_auth.current_user()


@users.route('/me', methods=['PUT'])
@authenticate(token_auth)
@body(update_user_schema)
@response(user_schema)
def put(data):
    """Edit user information"""
    user = token_auth.current_user()
    if 'password' in data and ('old_password' not in data or
                               not user.verify_password(data['old_password'])):
        abort(400)
    user.update(data)
    db.session.commit()
    return user


@users.route('/me/following', methods=['GET'])
@authenticate(token_auth)
@paginated_response(users_schema, order_by=User.username)
def my_following():
    """Retrieve the users the logged in user is following"""
    user = token_auth.current_user()
    return user.following_select()


@users.route('/me/followers', methods=['GET'])
@authenticate(token_auth)
@paginated_response(users_schema, order_by=User.username)
def my_followers():
    """Retrieve the followers of the logged in user"""
    user = token_auth.current_user()
    return user.followers_select()


@users.route('/me/following/<int:id>', methods=['GET'])
@authenticate(token_auth)
@response(EmptySchema, status_code=204,
          description='User is followed.')
@other_responses({404: 'User is not followed'})
def is_followed(id):
    """Check if a user is followed"""
    user = token_auth.current_user()
    followed_user = db.session.get(User, id) or abort(404)
    if not user.is_following(followed_user):
        abort(404)
    return {}


@users.route('/me/following/<int:id>', methods=['POST'])
@authenticate(token_auth)
@response(EmptySchema, status_code=204,
          description='User followed successfully.')
@other_responses({404: 'User not found', 409: 'User already followed.'})
def follow(id):
    """Follow a user"""
    user = token_auth.current_user()
    followed_user = db.session.get(User, id) or abort(404)
    if user.is_following(followed_user):
        abort(409)
    user.follow(followed_user)
    db.session.commit()
    return {}


@users.route('/me/following/<int:id>', methods=['DELETE'])
@authenticate(token_auth)
@response(EmptySchema, status_code=204,
          description='User unfollowed successfully.')
@other_responses({404: 'User not found', 409: 'User is not followed.'})
def unfollow(id):
    """Unfollow a user"""
    user = token_auth.current_user()
    unfollowed_user = db.session.get(User, id) or abort(404)
    if not user.is_following(unfollowed_user):
        abort(409)
    user.unfollow(unfollowed_user)
    db.session.commit()
    return {}


@users.route('/users/<int:id>/following', methods=['GET'])
@authenticate(token_auth)
@paginated_response(users_schema, order_by=User.username)
@other_responses({404: 'User not found'})
def following(id):
    """Retrieve the users this user is following"""
    user = db.session.get(User, id) or abort(404)
    return user.following_select()


@users.route('/users/<int:id>/followers', methods=['GET'])
@authenticate(token_auth)
@paginated_response(users_schema, order_by=User.username)
@other_responses({404: 'User not found'})
def followers(id):
    """Retrieve the followers of the user"""
    user = db.session.get(User, id) or abort(404)
    return user.followers_select()


@users.route('/users/application/<int:app_id>/episodes', methods=['GET'])
@authenticate(token_auth)
@response(episodes_user_schema, 201)
def episode_all(app_id):
    episodes = []
    user = token_auth.current_user()
    for episode in user.episode:
        if episode.episode.application_id == app_id:
            episodes.append(episode)
    # for app in user.application:
    #     if app.application_id == app_id:
    #         for episode in user.episode:
    #             print(episode)
    return episodes


@users.route('/users/episode/<int:ep_id>/lines', methods=['GET'])
@authenticate(token_auth)
@response(lines_user_schema, 201)
def lines_all(ep_id):
    lines = []
    user = token_auth.current_user()
    for line in user.lines:
        if line.lines.episode_id == ep_id:
            lines.append(line)
    # for app in user.application:
    #     if app.application_id == app_id:
    #         for episode in user.episode:
    #             print(episode)
    return lines


@users.route('/users/lines/<int:l_id>/update', methods=['PUT'])
@authenticate(token_auth)
@body(update_lines_user_schema)
@response(line_user_schema, 201)
def line_update(data, l_id):
    user = token_auth.current_user()
    line = db.session.query(LinesUserLink).filter_by(
        user_id=user.id, lines_id=l_id).one()
    line.state = data['state']
    line.current = data['current']
    line.current_char = data['current_char']
    line.current_line = data['current_line']
    db.session.add(line)
    db.session.commit()
    return ''


@users.route('/users/lines/<int:l_id>/finished', methods=['PUT'])
@authenticate(token_auth)
@body(update_lines_user_schema)
@response(line_user_schema, 201)
def line_finished(data, l_id):
    user = token_auth.current_user()
    line = db.session.query(LinesUserLink).filter_by(
        user_id=user.id, lines_id=l_id).one()
    print(line)
    print(data)
    line.state = data['state']
    line.current = data['current']
    line.current_char = data['current_char']
    line.current_line = data['current_line']
    db.session.add(line)
    next_line = db.session.query(LinesUserLink).filter_by(
        user_id=user.id).filter(LinesUserLink.lines_id > l_id).first()
    if next_line is not None:
        if line.lines.episodes.name == next_line.lines.episodes.name:
            next_line.current = True
            db.session.add(next_line)
    episode_id = line.lines.episodes.id
    ids = [line.id for line in line.lines.episodes.lines]
    print(ids)
    finished = [db.session.query(LinesUserLink).filter_by(
        user_id=user.id, lines_id=identificator).one().state for identificator in ids]
    print('finished', finished)
    response = all(finish == finished[0] for finish in finished)
    print('resp', response)
    if response:
        ep = db.session.query(EpisodeUserLink).filter_by(
            user_id=user.id, episode_id=episode_id).one()
        ep.is_finished = True
        db.session.add(ep)
    db.session.commit()
    application_id = line.lines.episodes.application.id
    ep_ids = [ep.id for ep in line.lines.episodes.application.episodes]
    print('ep_ids', ep_ids)
    app_finished = [db.session.query(EpisodeUserLink).filter_by(
        user_id=user.id, episode_id=ep_id).one().is_finished for ep_id in ep_ids]
    print('app_finished', app_finished)
    app_response = all(app_finish == app_finished[0] for app_finish in app_finished)
    print(app_response)
    if app_response:
        print('test', application_id)
        app = db.session.query(ApplicationUserLink).filter_by(
            user_id=user.id, application_id=application_id).one()
        app.is_finished = True
        print(app)
        db.session.add(app)
    db.session.commit()
    return ''


@users.route('/users/episode/<int:ep_id>/finished', methods=['PUT'])
@authenticate(token_auth)
@body(update_lines_user_schema)
@response(line_user_schema, 201)
def episode_finished(ep_id):
    return ''
