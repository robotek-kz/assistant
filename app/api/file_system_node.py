from flask import Blueprint, abort, request
from apifairy import authenticate, body, response, other_responses

from api import db
from api.models import  FileSystemNode, User
from api.schemas import FileSystemNodeSchema
from api.auth import token_auth
# from api.decorators import paginated_response
# from api.schemas import DateTimePaginationSchema



file_system_nodes = Blueprint('file_system_nodes', __name__)
file_system_node_schema = FileSystemNodeSchema()
file_system_nodes_schema = FileSystemNodeSchema(many=True)
update_file_system_node_schema = FileSystemNodeSchema(partial=True)


@file_system_nodes.route('/users/<int:id>/list-file-system-nodes', methods=['GET'])
@authenticate(token_auth)
@response(file_system_nodes_schema, 201)
def all(id):
    user = db.session.get(User, id) or abort(404)
    return db.session.scalars(user.file_system_nodes_select()).all()


@file_system_nodes.route('/users/create-file-system-nodes', methods=['POST'])
@authenticate(token_auth)
@body(file_system_node_schema)
@response(file_system_node_schema, 201)
def create(args):
    print(args)
    user = token_auth.current_user()
    temp = FileSystemNode(user=user, **args)
    db.session.add(temp)
    db.session.commit()
    return temp


@file_system_nodes.route('/users/update-file-system-nodes/<int:id>', methods=['PUT'])
@body(update_file_system_node_schema)
@response(file_system_node_schema, 201)
def put(data, id):
    print('request:', request.data)
    print('data:', data, 'id:', id)
    temp = db.session.get(FileSystemNode, id) or abort(404)
    temp.update(data)
    db.session.commit()
    return temp

@file_system_nodes.route('/users/delete-file-system-nodes/<int:id>', methods=['DELETE'])
@other_responses({403: 'Not allowed to delete the post'})
def delete(id):
    """Delete a post"""
    temp = db.session.get(FileSystemNode, id) or abort(404)
    db.session.delete(temp)
    db.session.commit()
    return '', 204