from flask import Blueprint, abort
from apifairy import authenticate, body, response, other_responses

from api import db
from api.models import  GameSketch, User, FileGameSketch, UserGameSketchScores
from api.schemas import GameSketchSchema
from api.auth import token_auth
from api.decorators import paginated_response
from api.schemas import DateTimePaginationSchema



game_sketches = Blueprint('game_sketches', __name__)
game_sketch_schema = GameSketchSchema()
game_sketches_schema = GameSketchSchema(many=True)
update_game_sketches_schema = GameSketchSchema(partial=True)


@game_sketches.route('/users/<int:id>/game_sketches', methods=['GET'])
@authenticate(token_auth)
@paginated_response(game_sketch_schema, order_by=GameSketch.timestamp,
                    order_direction='desc',
                    pagination_schema=DateTimePaginationSchema)
@other_responses({404: 'User not found'})
def user_all(id):
    """Retrieve all posts from a user"""
    user = db.session.get(User, id) or abort(404)
    return user.game_sketches_select()


@game_sketches.route('/game_sketches/<int:id>', methods=['PUT'])
@authenticate(token_auth)
@body(update_game_sketches_schema)
@response(game_sketch_schema)
@other_responses({403: 'Not allowed to edit this post',
                  404: 'Post not found'})
def put(data, id):
    """Обновить состояние модели <GameSketch>"""
    print('privet', data, id)
    game_sketch = db.session.get(GameSketch, id) or abort(404)
    if game_sketch.user != token_auth.current_user():
        abort(403)
    files = db.session.get(FileGameSketch, game_sketch.file_game_sketch_id) or abort(404)
    if data['is_done'] == 'finished':
        number = game_sketch.number + 1
        for i in files.game_sketches:
            if i.number == number:
                i.update({'current': True})
                i.user.user_game_sketch_scores.append(UserGameSketchScores(game_sketch=i,score=i.score))
                
    game_sketch.update(data)
    db.session.commit()
    count = 0
    for i in files.game_sketches:
        if i.is_done == 'finished':
            count += 1
    if count == len(files.game_sketches):
        # todo исправить потом
        files.project_game_sketches.is_done = True
        files.is_done = True
        db.session.add(files)
        db.session.commit()
        print(files.project_game_sketches.is_done)
    return game_sketch