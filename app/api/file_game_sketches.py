from flask import Blueprint, abort
from apifairy import authenticate, body, response, other_responses

from api import db
from api.models import  FileGameSketch, User
from api.schemas import FileGameSketchSchema
from api.auth import token_auth
from api.decorators import paginated_response
from api.schemas import DateTimePaginationSchema



file_game_sketches = Blueprint('file_game_sketches', __name__)
file_game_sketch_schema = FileGameSketchSchema()
file_game_sketches_schema = FileGameSketchSchema(many=True)
update_file_game_sketches_schema = FileGameSketchSchema(partial=True)


@file_game_sketches.route('/users/<int:id>/file_game_sketches', methods=['GET'])
@authenticate(token_auth)
@paginated_response(file_game_sketch_schema, order_by=FileGameSketch.timestamp,
                    order_direction='desc',
                    pagination_schema=DateTimePaginationSchema)
@other_responses({404: 'User not found'})
def user_all(id):
    """Retrieve all file game sketches from a user"""
    user = db.session.get(User, id) or abort(404)
    return user.file_game_sketches_select()


@file_game_sketches.route('/file_game_sketches/<int:id>', methods=['PUT'])
@authenticate(token_auth)
@body(update_file_game_sketches_schema)
@response(file_game_sketch_schema)
@other_responses({403: 'Not allowed to edit this file game sketch',
                  404: 'Post not found'})
def put(data, id):
    """Edit a post"""
    file_game_sketch = db.session.get(FileGameSketch, id) or abort(404)
    print("FILE_GAME_SKETHC", file_game_sketch)
    if file_game_sketch.user != token_auth.current_user():
        abort(403)
    print("DAAAAAAATA", data, id)
    file_game_sketch.update(data)
    db.session.commit()
    return file_game_sketch