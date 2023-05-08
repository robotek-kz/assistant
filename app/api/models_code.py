


# class User():

#     id = Integer
#     username = String(64)

#     password_hash = String(128)
#     scores = Score()


# class Score():

#     id = Integer()
#     point = Integer()

# class Project():


#     id = Integer()
#     name = String()
#     lesson = Lesson()



# class Lesson():

#     id = Integer()
#     name = String()
#     ext = String()
#     mode = String()
#     description = Text()
#     files = CodeFiles()

# class CodeFiles():

#     id = Integer()
#     name = String()
#     source_name = String()
#     source = String()
#     tab_size = Integer
#     lines = Integer() 

# class Day():

#     id = Integer()
#     project = Project()


from datetime import datetime, timedelta
# from hashlib import md5
# import secrets
# from time import time
# from turtle import back

# from flask import current_app, url_for

# import jwt
import sqlalchemy as sqla
from sqlalchemy import orm as sqla_orm
# from werkzeug.security import generate_password_hash, check_password_hash

# from api.app import db
engine = sqla.create_engine('sqlite:///:memory:')
Base = sqla_orm.declarative_base()

class User(Base):
    __tablename__ = 'users'


    id = sqla.Column(sqla.Integer, primary_key = True)
    name = sqla.Column(sqla.String(128))
    password_hash = sqla.Column(sqla.String(256))
    first_seen = sqla.Column(sqla.DateTime, default=datetime.utcnow)
    last_seen = sqla.Column(sqla.DateTime, default=datetime.utcnow)


class Lesson(Base):
    __tablename__ = 'lessons'


    id = sqla.Column(sqla.Integer, primary_key = True)
    name = sqla.Column(sqla.String(64), nullable = False)
    ext = sqla.Column(sqla.String(10), index = True, nullable = False)
    mode = sqla.Column(sqla.String(32), index = True, nullable = False)
    description = sqla.Column(sqla.Text)
    code_files = sqla_orm.relationship('CodeFile')


class CodeFile(Base):
    __tablename__ = 'code_files'

    id = sqla.Column(sqla.Integer, primary_key = True)
    name = sqla.Column(sqla.String(64), nullable = False)
    description = sqla.Column(sqla.Text)
    source = sqla.Column(sqla.Text(), nullable = False)
    source_name = sqla.Column(sqla.String(64), nullable = False)
    tab_size = sqla.Column(sqla.Integer, nullable = False)
    lines = sqla.Column(sqla.Integer, nullable = False)
    score = sqla.Column(sqla.Integer)
    lesson_id = sqla.Column(sqla.Integer, sqla.ForeignKey(Lesson.id), index = True)


class User_CodeFile(Base):
    __tablename__ = 'user_code_files'

    id = sqla.Column(sqla.Integer, primary_key = True, autoincrement = True)
    user_id = sqla.Column(sqla.Integer, sqla.ForeignKey(User.id), primary_key = True)
    code_file_id = sqla.Column(sqla.Integer, sqla.ForeignKey(CodeFile.id), primary_key = True)
    is_done = sqla.Column(sqla.Boolean, default = False)
    user = sqla_orm.relationship("User", backref=sqla_orm.backref("user_code_files"))
    code_file = sqla_orm.relationship("CodeFile", backref=sqla_orm.backref("user_code_files"))


if __name__ == '__main__':

    Base.metadata.create_all(engine)
    Session = sqla_orm.sessionmaker(bind=engine)
    session = Session()

    u = User()
    u.name = ''
    l = Lesson()
    import pdb
    pdb.set_trace()
    # session.add(u)
    # session.commit()
    # print(u.name)