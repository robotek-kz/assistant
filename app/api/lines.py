from flask import Blueprint, abort, request, jsonify
from apifairy import authenticate, body, response, other_responses
import uuid
import os
from api import db
from api.models import Episode, Lines
from api.schemas import LinesSchema, DataLineSchema
# from api.auth import token_auth
# from api.decorators import paginated_response
# from api.schemas import DateTimePaginationSchema


lines = Blueprint('lines', __name__)
line_schema = LinesSchema()
lines_schema = LinesSchema(many=True)
data_lines_schema = DataLineSchema(many=True)
# files_code_schema = FilesCodeSchema(many=True)
# update_file_schema = UpdateFilesSchema()
# update_file_system_node_schema = FileSystemNodeSchema(partial=True)


@lines.route('/episode/<int:id>/lines', methods=['GET'])
# @authenticate(token_auth)
@response(lines_schema, 201)
def episode_all(id):
    episode = db.session.get(Episode, id)
    # array = db.session.scalars(episode.files_select()).all()
    # temp = []
    # for y, i in enumerate(array):
    #     data = { "id": i.id, "path": i.path, "code": i.read() }
    #     temp.append(data)
    return db.session.scalars(episode.lines_select()).all()


@lines.route('/episode/<int:id>/lines', methods=['POST'])
@body(lines_schema)
def upload(args, id):
    episode = db.session.get(Episode,id)
    for arg in args:
        lines = Lines(episodes=episode, **arg)
        db.session.add(lines)
    db.session.commit()
    return 'Completed', 201


# @files.route('/files/<int:id>', methods=['GET'])
# @response(file_schema, 200)
# def get(id):
#     """Retrieve a files by id"""
#     return db.session.get(Files, id) or abort(404)


# @files.route('/files/<int:id>', methods=['PUT'])
# @body(update_file_schema)
# @response(update_file_schema, 201)
# def put(data, id):
#     """Update a files by id"""
#     file = db.session.get(Files, id) or abort(404)
#     file.update(data)
#     db.session.commit()
#     return files


# @files.route('/files/<int:id>', methods=['DELETE'])
# @other_responses({403: 'Not allowed to delete the files'})
# def delete(id):
#     """Delete a files"""
#     file = db.session.get(Files, id) or abort(404)
#     db.session.delete(file)
#     db.session.commit()
#     return '', 204
