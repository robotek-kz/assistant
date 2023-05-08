from flask import Blueprint, abort, request
from apifairy import authenticate, body, response, other_responses
import uuid
import os
import shutil
from api import db
from api.models import  Application, Episode
from api.schemas import EpisodeSchema
# from api.schemas import FilesSchema
# from api.auth import token_auth
# from api.decorators import paginated_response
# from api.schemas import DateTimePaginationSchema


episode = Blueprint('episode', __name__)
episode_schema = EpisodeSchema()
episodes_schema = EpisodeSchema(many=True)
# file_schema = FilesSchema()
# files_schema = FilesSchema(many=True)
# update_file_system_node_schema = FileSystemNodeSchema(partial=True)

@episode.route('/application/<int:id>/episode', methods=['POST'])
@body(episode_schema)
@response(episode_schema, 201)
def new(args, id):
    """Create a new episode"""
    application = db.session.get(Application, id)
    episode = Episode(application = application, **args)
    db.session.add(episode)
    db.session.commit()
    folderPath = 'uploads/applications/' + application.path + '/' + args['path']
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    return episode


@episode.route('/application/<int:id>/episodes', methods=['GET'])
@response(episodes_schema, 200)
def application_all(id):
    """Retrieve all applications"""
    application = db.session.get(Application, id)
    return db.session.scalars(application.episode_select()).all()


@episode.route('/episode/<int:id>', methods=['GET'])
@response(episode_schema, 200)
def get(id):
    """Retrieve an application by id"""
    return db.session.get(Episode, id) or abort(404)


@episode.route('/episode/<int:id>', methods=['PUT'])
@body(episode_schema)
@response(episode_schema, 201)
def put(data, id):
    """Update an application by id"""
    print(data)
    episode = db.session.get(Episode, id) or abort(404)
    os.rename('uploads/applications/' + episode.application.path + '/' + episode.path, \
               'uploads/applications/' + episode.application.path + '/' + data['path'])
    # for file in episode.files:
    #     os.rename('/'.join(file.path.split('/')[:4]), \
    #             'uploads/applications/' + episode.application.path + '/' + data['path'])
    episode.update(data)
    db.session.commit()
    return episode

@episode.route('/episode/<int:id>', methods=['DELETE'])
@other_responses({403: 'Not allowed to delete the episode'})
def delete(id):
    """Delete an application"""
    episode = db.session.get(Episode, id) or abort(404)
    folderPath = 'uploads/applications/' + episode.application.path + '/' + episode.path
    try:
        shutil.rmtree(folderPath)
    except:
        pass
    db.session.delete(episode)
    db.session.commit()
    return '', 204