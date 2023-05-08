from flask import Blueprint, abort, request
from apifairy import authenticate, body, response, other_responses
from sqlalchemy import text
import uuid
import os
import shutil
from api import db
from api.models import  Application, Files, GameApplication, GameEpisode, GameFiles, GameLines, User, ApplicationUserLink, EpisodeUserLink, LinesUserLink, User
from api.schemas import ApplicationSchema, IdSchema, UserSchema
from api.schemas import FilesSchema
# from api.auth import token_auth
# from api.decorators import paginated_response
# from api.schemas import DateTimePaginationSchema


application = Blueprint('application', __name__)
application_schema = ApplicationSchema()
applications_schema = ApplicationSchema(many=True)
file_schema = FilesSchema()
files_schema = FilesSchema(many=True)
id_schema = IdSchema()
users_schema = UserSchema(many=True)
# update_file_system_node_schema = FileSystemNodeSchema(partial=True)
def name_exists(name):
    a = db.session.execute(db.session.query(Application).filter(Application.name == name)).all()
    print(a)
    return db.session.query(Application).filter(Application.name == name)
@application.route('/application', methods=['POST'])
@body(application_schema)
@response(application_schema, 201)
def new(args):
    """Create a new application"""
    # if name_exists(args['name']):
    #     return {'error': 'User with this email already exists'}, 422
    application = Application(**args)
    db.session.add(application)
    db.session.commit()
    folderPath = 'uploads/applications/' + args['path']
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    return application


@application.route('/application', methods=['GET'])
@response(applications_schema, 200)
def all():
    """Retrieve all applications"""
    return db.session.scalars(Application.select()).all()


@application.route('/application/<int:id>', methods=['GET'])
@response(application_schema, 200)
def get(id):
    """Retrieve an application by id"""
    return db.session.get(Application, id) or abort(404)


@application.route('/application/<int:id>', methods=['PUT'])
@body(application_schema)
@response(application_schema, 201)
def put(data, id):
    """Update an application by id"""
    application = db.session.get(Application, id) or abort(404)
    os.rename('uploads/applications/' + application.path, \
               'uploads/applications/' + data['name'])
    application.update(data)
    db.session.commit()
    return application

@application.route('/application/<int:id>', methods=['DELETE'])
@other_responses({403: 'Not allowed to delete the application'})
def delete(id):
    """Delete an application"""
    application = db.session.get(Application, id) or abort(404)
    folderPath = 'uploads/applications/' + application.path
    try:
        shutil.rmtree(folderPath)
    except:
        pass
    db.session.delete(application)
    db.session.commit()
    return '', 204


def is_subset(subset, superset):
    return set(subset) <= set(superset)
@application.route('/application/<int:id>/create', methods=['POST'])
@body(id_schema)
@response(users_schema, 201)
def create_for_user(data,id):
    application = db.session.get(Application, id) or abort(404)
    users = db.session.scalars(User.select()).all()
    for user_id in data['ids']:
        user = db.session.get(User, user_id) or abort(404)
        app_2 = [app.application_id for app in user.application]
        if is_subset([application.id], app_2):
            for episode in application.episodes:
                id_1 = [episode.id for episode in application.episodes]
                id_2 = [episode.episode_id for episode in user.episode]
                if not is_subset(id_1, id_2):
                    e = EpisodeUserLink(is_finished=False)
                    e.episode = episode
                    user.episode.append(e)
                for lines in episode.lines:
                    l = LinesUserLink(is_finished=False)
                    l.lines = lines
                    user.lines.append(l)          
        else:
            a = ApplicationUserLink(is_finished=False)
            a.application = application
            user.application.append(a)
            for episode in application.episodes:
                e = EpisodeUserLink(is_finished=False)
                e.episode = episode
                user.episode.append(e)
                for lines in episode.lines:
                    current = False
                    if lines.number == 1:
                        current = True
                    l = LinesUserLink(is_finished=False, state='init', current_line=0, current_char=0, current=current)
                    l.lines = lines
                    user.lines.append(l)
    db.session.commit()
    return users

# @application.route('/application/<int:id>/create', methods=['GET'])
# def create_game(id):
#     application = db.session.get(Application, id) or abort(404)
#     # print(application.name, application.description)
#     game_application = GameApplication(
#         name = application.name,
#         description = application.description,
#         is_finished = False,
#         path = application.path
#     )
#     db.session.add(game_application)
#     for episode in application.episodes:
#         game_episode = GameEpisode(
#             name=episode.name,
#             path=episode.path,
#             game_application=game_application
#         )
#         db.session.add(game_episode)
#         # print('episode', episode.name, episode.path)
#         for file in episode.files:
#             game_file = GameFiles(
#                 name=file.name,
#                 path=file.path,
#                 game_episodes=game_episode
#             )
#             db.session.add(game_file)
#             #print('file:',file.id, file.name, file.episode_id)
#         for line in episode.lines:
#             game_line = GameLines(
#                 name=line.name,
#                 number=line.number,
#                 current=line.current,
#                 code=line.code,
#                 ext=line.ext,
#                 mode=line.mode,
#                 file_name=line.file_name,
#                 file_source=line.file_source,
#                 file_tab_size=line.file_tab_size,
#                 file_lines=line.file_lines,
#                 score=line.score,
#                 game_episodes=game_episode
#             )
#             db.session.add(game_line)
#     db.session.commit()
#             #print('line:', line.episode_id, line.id, line.name, line.number, line.current, line.code, line.ext, line.mode, line.file_name, line.file_source, line.file_tab_size, line.file_lines, line.score)
#     return 'body'
# @application.route('/files', methods=['POST'])
# @body(file_schema, location='files')
# @response(file_schema, 201)
# def new_file(args):
#     """Create a new files"""
#     print(request.files)
#     # files = Files(**args)
#     # db.session.add(files)
#     # db.session.commit()
#     return 'created'