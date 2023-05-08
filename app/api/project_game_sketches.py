from flask import Blueprint, abort
from apifairy import authenticate, body, response, other_responses

from api import db
from api.models import  ProjectGameSketch, User
from api.schemas import ProjectGameSketchSchema
from api.auth import token_auth
from api.decorators import paginated_response
from api.schemas import DateTimePaginationSchema



project_game_sketches = Blueprint('project_game_sketches', __name__)
project_game_sketch_schema = ProjectGameSketchSchema()
project_game_sketches_schema = ProjectGameSketchSchema(many=True)
update_project_game_sketches_schema = ProjectGameSketchSchema(partial=True)


@project_game_sketches.route('/users/<int:id>/project_game_sketches', methods=['GET'])
@authenticate(token_auth)
@paginated_response(project_game_sketch_schema, order_by=ProjectGameSketch.timestamp,
                    order_direction='desc',
                    pagination_schema=DateTimePaginationSchema)
@other_responses({404: 'User not found'})
def user_all(id):
    """Вытащить данные из модели <ProjectGameSketch>"""
    user = db.session.get(User, id) or abort(404)
    return user.project_game_sketches_select()


# @game_sketches.route('/users/<int:id>/project_game_sketches', methods=['PUT'])
# @authenticate(token_auth)
# @body(update_game_sketches_schema)
# @response(game_sketch_schema)
# @other_responses({403: 'Not allowed to edit this post',
#                   404: 'Post not found'})
# def put(data, id):
#     """Edit a post"""
#     game_sketch = db.session.get(GameSketch, id) or abort(404)
#     if game_sketch.user != token_auth.current_user():
#         abort(403)
#     game_sketch.update(data)
#     db.session.commit()
#     return game_sketch