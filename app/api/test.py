from flask import Blueprint, render_template

from api.app import db
from api.models import User

test = Blueprint('test',__name__)

@test.route('/test')
def index():
    with db.Session() as session:
        users = session.scalars(User.select())
        return render_template('test.html', users=users)