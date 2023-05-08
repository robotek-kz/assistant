from flask import Blueprint, abort
from apifairy import authenticate, body, response, other_responses

from api import db
from api.models import  TemplateSketch
from api.schemas import TemplateSketchSchema
from api.auth import token_auth
from api.decorators import paginated_response
from api.schemas import DateTimePaginationSchema



template_sketches = Blueprint('template_sketches', __name__)
template_sketch_schema = TemplateSketchSchema()
template_sketches_schema = TemplateSketchSchema(many=True)
# template_get_sketch_schema = TemplatetSketchCodeSchema(partial=True)



@template_sketches.route('/template_sketches', methods=['POST'])
@authenticate(token_auth)
@body(template_sketch_schema)
@response(template_sketch_schema, 201)
def new(args):
    template_sketch = TemplateSketch(**args)
    db.session.add(template_sketch)
    db.session.commit()
    return template_sketch

@template_sketches.route('/template_sketches/<int:id>', methods=['GET'])
@authenticate(token_auth)
@response(template_sketch_schema)
@other_responses({404: 'Sketch not found'})
def get(id):
    return db.session.get(TemplateSketch, id) or abort(404)

@template_sketches.route('/template_sketches', methods=['GET'])
@authenticate(token_auth)
@paginated_response(template_sketch_schema, order_by=TemplateSketch.timestamp,
                    order_direction='desc',
                    pagination_schema=DateTimePaginationSchema)
def all():
    return TemplateSketch.select()


