from flask import Blueprint, abort, request, jsonify, send_from_directory, send_file
from apifairy import authenticate, body, response, other_responses
import uuid
import os
from api import db
from api.models import Episode, Files, Application
from api.schemas import FilesSchema, FileNameSchema, FilesCodeSchema, UpdateFilesSchema, EpisodeSchema, ApplicationFilesSchema, ApplicationFileNameSchema
# from api.auth import token_auth
# from api.decorators import paginated_response
# from api.schemas import DateTimePaginationSchema


files = Blueprint('files', __name__)
file_schema = FilesSchema()
files_schema = FilesSchema(many=True)
files_name_schema = FileNameSchema(many=True)
files_code_schema = FilesCodeSchema(many=True)
update_file_schema = UpdateFilesSchema()
episode_schema = EpisodeSchema()
application_file_schema = ApplicationFilesSchema()
application_files_schema = ApplicationFilesSchema(many=True)
application_files_name_schema = ApplicationFileNameSchema(many=True)
# update_file_system_node_schema = FileSystemNodeSchema(partial=True)


@files.route('/episode/<int:id>/files', methods=['GET'])
# @authenticate(token_auth)
@response(files_code_schema, 201)
def episode_all(id):
    episode = db.session.get(Episode, id)
    # array = db.session.scalars(episode.files_select()).all()
    # temp = []
    # for y, i in enumerate(array):
    #     data = { "id": i.id, "path": i.path, "code": i.read() }
    #     temp.append(data)
    return db.session.scalars(episode.files_select()).all()
@files.route('/application/<int:id>/files/download', methods=['GET'])
def download_file(id):
    application = db.session.get(Application, id)
    try:
        return send_file('../uploads/applications' + '/' + application.path + '/' + application.files[0].path, as_attachment=True)
    except IndexError:
        return ''
@files.route('/application/<int:id>/files', methods=['POST'])
@body(application_file_schema, location='files')
@response(application_files_name_schema, 201)
def applicatiaon_upload(args, id):
    application = db.session.get(Application, id)
    folderPath = 'uploads/applications/' + application.path
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    all_files = request.files.getlist('files')
    files = []
    for one in all_files:
        one.save(os.path.join(folderPath, one.filename))
        file = Files(name=one.filename, path=one.filename, application=application)
        db.session.add(file)
        files.append(file)
    db.session.commit()
    return files

@files.route('/episode/<int:id>/files', methods=['POST'])
@body(file_schema, location='files')
@response(files_name_schema, 201)
def upload(args, id):
    episode = db.session.get(Episode, id)
    folderPath = 'uploads/applications/' + \
        episode.application.name + '/' + episode.name
    # folderPath =  'uploads/applications/' + 
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    all_files = request.files.getlist('py')
    files = []
    for one in all_files:
        one.save(os.path.join(folderPath, one.filename))
        file = Files(name=one.filename, path=one.filename, episode=episode)
        db.session.add(file)
        files.append(file)
    db.session.commit()
    return files


@files.route('/files/<int:id>', methods=['GET'])
@response(file_schema, 200)
def get(id):
    """Retrieve a files by id"""
    return db.session.get(Files, id) or abort(404)


@files.route('/files/<int:id>', methods=['PUT'])
@body(update_file_schema)
@response(update_file_schema, 201)
def put(data, id):
    """Update a files by id"""
    file = db.session.get(Files, id) or abort(404)
    file.update(data)
    db.session.commit()
    return files


@files.route('/files/<int:id>', methods=['DELETE'])
@other_responses({403: 'Not allowed to delete the files'})
def delete(id):
    """Delete a files"""
    file = db.session.get(Files, id) or abort(404)
    db.session.delete(file)
    db.session.commit()
    return '', 204
