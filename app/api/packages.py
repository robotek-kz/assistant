import uuid
import os
from flask import Blueprint, abort, request
from apifairy import authenticate, body, response, other_responses

from api import db
from api.models import  Packages
from api.schemas import PackagesSchema
from api.auth import token_auth



packages = Blueprint('packages', __name__)
package_schema = PackagesSchema()
packages_schema = PackagesSchema(many=True)


@packages.route('/packages', methods=['GET'])
@response(packages_schema, 201)
def all():
    return db.session.scalars(Packages.select()).all()

@packages.route('/upload', methods=['POST'])
@body(package_schema, location='form')
@response(package_schema, 201)
def upload(args):
    uploadID = uuid.uuid4().hex[0:9]
    folderPath = 'uploads'+'/'+ uploadID
    os.makedirs(folderPath)
    args['wheel'].save(os.path.join('uploads', uploadID, args['wheel'].filename))
    package = Packages(name=args['wheel'].filename,path=uploadID+'/'+args['wheel'].filename)
    db.session.add(package)
    db.session.commit()
    return package
