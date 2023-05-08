from flask import Blueprint, abort
from apifairy import authenticate, body, response, other_responses

from api import db
from api.models import User, Sketch
from api.schemas import SketchSchema
from api.auth import token_auth
from api.decorators import paginated_response
from api.schemas import DateTimePaginationSchema



sketches = Blueprint('sketches', __name__)
sketch_schema = SketchSchema()
sketches_schema = SketchSchema(many=True)
update_sketch_schema = SketchSchema(partial=True)



@sketches.route('/sketches', methods=['POST'])
@authenticate(token_auth)
@body(sketch_schema)
@response(sketch_schema, 201)
def new(args):
    user = token_auth.current_user()
    sketch = Sketch(author=user, **args)
    db.session.add(sketch)
    db.session.commit()
    return sketch

@sketches.route('/sketches/<int:id>', methods=['GET'])
@authenticate(token_auth)
@response(sketch_schema)
@other_responses({404: 'Sketch not found'})
def get(id):
    return db.session.get(Sketch, id) or abort(404)

@sketches.route('/sketches', methods=['GET'])
@authenticate(token_auth)
@paginated_response(sketch_schema, order_by=Sketch.timestamp,
                    order_direction='desc',
                    pagination_schema=DateTimePaginationSchema)
def all():
    return Sketch.select()


@sketches.route('/users/<int:id>/sketches', methods=['GET'])
@authenticate(token_auth)
@paginated_response(sketches_schema,order_by=Sketch.timestamp,
                            order_direction='desc',
                            pagination_schema=DateTimePaginationSchema)
@other_responses({404: 'Пользователь не найден'})
def user_all(id):
    user = db.session.get(User, id) or abort(404)

    return user.sketches_select()
