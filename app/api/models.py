from datetime import datetime, timedelta
from hashlib import md5
import secrets
from time import time
from collections import OrderedDict
from flask import current_app, url_for
import jwt
import sqlalchemy as sqla
from sqlalchemy import orm as sqla_orm
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_method
import enum
from api.app import db
import difflib

class Updateable:
    def update(self, data):
        for attr, value in data.items():
            setattr(self, attr, value)


followers = sqla.Table(
    'followers',
    db.Model.metadata,
    sqla.Column('follower_id', sqla.Integer, sqla.ForeignKey('users.id')),
    sqla.Column('followed_id', sqla.Integer, sqla.ForeignKey('users.id'))
)



class Token(db.Model):
    __tablename__ = 'tokens'

    id = sqla.Column(sqla.Integer, primary_key=True)
    access_token = sqla.Column(sqla.String(64), nullable=False, index=True)
    access_expiration = sqla.Column(sqla.DateTime, nullable=False)
    refresh_token = sqla.Column(sqla.String(64), nullable=False, index=True)
    refresh_expiration = sqla.Column(sqla.DateTime, nullable=False)
    user_id = sqla.Column(sqla.Integer, sqla.ForeignKey('users.id'),
                          index=True)

    user = sqla_orm.relationship('User', back_populates='tokens')

    def generate(self):
        self.access_token = secrets.token_urlsafe()
        self.access_expiration = datetime.utcnow() + \
            timedelta(minutes=current_app.config['ACCESS_TOKEN_MINUTES'])
        self.refresh_token = secrets.token_urlsafe()
        self.refresh_expiration = datetime.utcnow() + \
            timedelta(days=current_app.config['REFRESH_TOKEN_DAYS'])

    def expire(self):
        self.access_expiration = datetime.utcnow()
        self.refresh_expiration = datetime.utcnow()

    @staticmethod
    def clean():
        """Remove any tokens that have been expired for more than a day."""
        yesterday = datetime.utcnow() - timedelta(days=1)
        db.session.execute(Token.delete().where(
            Token.refresh_expiration < yesterday))


class User(Updateable, db.Model):
    __tablename__ = 'users'

    id = sqla.Column(sqla.Integer, primary_key=True)
    username = sqla.Column(sqla.String(64), index=True, unique=True,
                           nullable=False)
    email = sqla.Column(sqla.String(120), index=True, unique=True)
    nickname = sqla.Column(sqla.String(128), index=True, unique=True,
                            nullable=False)
    role = sqla.Column(sqla.Enum('admin','student'), default='student')
    password_hash = sqla.Column(sqla.String(128))
    about_me = sqla.Column(sqla.String(140))
    first_seen = sqla.Column(sqla.DateTime, default=datetime.utcnow)
    last_seen = sqla.Column(sqla.DateTime, default=datetime.utcnow)
    tokens = sqla_orm.relationship('Token', back_populates='user',
                                   lazy='noload')
    application = sqla_orm.relationship("ApplicationUserLink", back_populates="user")
    episode = sqla_orm.relationship("EpisodeUserLink", back_populates="user")
    lines = sqla_orm.relationship("LinesUserLink", back_populates="user")
    game_application = sqla_orm.relationship('GameApplication', back_populates='user')
    # posts = sqla_orm.relationship('Post', back_populates='author',
    #                               lazy='noload')
    # scores = sqla_orm.relationship('Score', back_populates='user')
    sketches = sqla_orm.relationship('Sketch', back_populates='author',
                                    lazy='noload')
    project_game_sketches = sqla_orm.relationship('ProjectGameSketch', back_populates='user')
    file_game_sketches = sqla_orm.relationship('FileGameSketch', back_populates='user')
    game_sketches = sqla_orm.relationship('GameSketch', back_populates='user')
    file_system_nodes = sqla_orm.relationship('FileSystemNode', back_populates='user')
    _total_xp = sqla.Column(sqla.Integer)
    @property
    def total_xp(self):
        return sum([score.score for score in self.user_game_sketch_scores])

    user_game_sketch_scores = sqla_orm.relationship(
        "UserGameSketchScores", cascade="all, delete-orphan", backref="user"
    )
    following = sqla_orm.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        back_populates='followers', lazy='noload')
    followers = sqla_orm.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        back_populates='following', lazy='noload')

    def project_game_sketches_select(self):
        return ProjectGameSketch.select().where(sqla_orm.with_parent(self, User.project_game_sketches))

    def file_game_sketches_select(self):
        return FileGameSketch.select().where(sqla_orm.with_parent(self, User.file_game_sketches))

    def game_sketches_select(self):
        return GameSketch.select().where(sqla_orm.with_parent(self, User.game_sketches))

    def file_system_nodes_select(self):
        return FileSystemNode.select().where(sqla_orm.with_parent(self, User.file_system_nodes))

    def sketches_select(self):
        return Sketch.select().where(sqla_orm.with_parent(self, User.sketches))

    # def posts_select(self):
    #     return Post.select().where(sqla_orm.with_parent(self, User.posts))

    def following_select(self):
        return User.select().where(sqla_orm.with_parent(self, User.following))

    def followers_select(self):
        return User.select().where(sqla_orm.with_parent(self, User.followers))

    def xperience(self):
        return self.total_xp

    # def followed_posts_select(self):
    #     return Post.select().join(
    #         followers, (followers.c.followed_id == Post.user_id),
    #         isouter=True).group_by(Post.id).filter(
    #             sqla.or_(Post.author == self,
    #                      followers.c.follower_id == self.id))

    def __repr__(self):  # pragma: no cover
        return '<User {}>'.format(self.username)

    @property
    def url(self):
        return url_for('users.get', id=self.id)

    @property
    def avatar_url(self):
        digest = md5(self.nickname.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon'

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def ping(self):
        self.last_seen = datetime.utcnow()

    def generate_auth_token(self):
        token = Token(user=self)
        token.generate()
        return token

    @staticmethod
    def verify_access_token(access_token, refresh_token=None):
        token = db.session.scalar(Token.select().filter_by(
            access_token=access_token))
        if token:
            if token.access_expiration > datetime.utcnow():
                token.user.ping()
                db.session.commit()
                return token.user

    @staticmethod
    def verify_refresh_token(refresh_token, access_token):
        token = db.session.scalar(Token.select().filter_by(
            refresh_token=refresh_token, access_token=access_token))
        if token:
            if token.refresh_expiration > datetime.utcnow():
                return token

            # someone tried to refresh with an expired token
            # revoke all tokens from this user as a precaution
            token.user.revoke_all()
            db.session.commit()

    def revoke_all(self):
        db.session.execute(Token.delete().where(Token.user == self))

    def generate_reset_token(self):
        return jwt.encode(
            {
                'exp': time() + current_app.config['RESET_TOKEN_MINUTES'] * 60,
                'reset_email': self.email,
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    @staticmethod
    def verify_reset_token(reset_token):
        try:
            data = jwt.decode(reset_token, current_app.config['SECRET_KEY'],
                              algorithms=['HS256'])
        except jwt.PyJWTError:
            return
        return db.session.scalar(User.select().filter_by(
            email=data['reset_email']))

    def follow(self, user):
        if not self.is_following(user):
            db.session.execute(followers.insert().values(
                follower_id=self.id, followed_id=user.id))

    def unfollow(self, user):
        if self.is_following(user):
            db.session.execute(followers.delete().where(
                followers.c.follower_id == self.id,
                followers.c.followed_id == user.id))

    def is_following(self, user):
        return db.session.scalars(User.select().where(
            User.id == self.id, User.following.contains(
                user))).one_or_none() is not None


# class Score(db.Model):
#     __tablename__ = 'scores'

#     id = sqla.Column(sqla.Integer, primary_key = True)
#     xp = sqla.Column(sqla.Integer)

    # user_id = sqla.Column(sqla.Integer, sqla.ForeignKey(User.id), index=True)

    # user = sqla_orm.relationship('User', back_populates='scores')

class ProjectGameSketch(Updateable, db.Model):
    __tablename__ = 'project_game_sketches'

    id = sqla.Column(sqla.Integer, primary_key = True)
    name = sqla.Column(sqla.String(128))
    description = sqla.Column(sqla.String(128))
    gif_path = sqla.Column(sqla.String)
    # code = sqla.Column(sqla.Text)
    timestamp = sqla.Column(sqla.DateTime, index=True, default=datetime.utcnow,
                            nullable=False)
    is_done = sqla.Column(sqla.Boolean, default=False)
    path = sqla.Column(sqla.String)
    # game_sketches = sqla_orm.relationship('GameSketch', back_populates='project_game_sketches')
    file_game_sketches = sqla_orm.relationship('FileGameSketch', back_populates='project_game_sketches')
    user_id = sqla.Column(sqla.Integer, sqla.ForeignKey(User.id), index=True)
    user = sqla_orm.relationship('User', back_populates='project_game_sketches')

class FileGameSketch(Updateable, db.Model):
    __tablename__ = 'file_game_sketches'

    id = sqla.Column(sqla.Integer, primary_key = True)
    name = sqla.Column(sqla.String(64))
    code = sqla.Column(sqla.Text)
    previous_code = sqla.Column(sqla.Text)
    timestamp = sqla.Column(sqla.DateTime, index=True, default=datetime.utcnow,
                            nullable=False)
    # lines = sqla.Column(sqla.Integer)
    is_done = sqla.Column(sqla.Boolean, default=False)
    project_game_sketch_id = sqla.Column(sqla.Integer, sqla.ForeignKey(ProjectGameSketch.id), index=True)
    project_game_sketches = sqla_orm.relationship('ProjectGameSketch', back_populates='file_game_sketches')
    game_sketches = sqla_orm.relationship('GameSketch', back_populates='file_game_sketches')
    user_id = sqla.Column(sqla.Integer, sqla.ForeignKey(User.id), index=True)
    user = sqla_orm.relationship('User', back_populates='file_game_sketches')

    # def __init__(self, name, code, project_game_sketches, user):
    #     self.name = name
    #     # self.lines = lines
    #     self.code = code
    #     self.project_game_sketches = project_game_sketches
    #     self.user = user





class GameSketch(Updateable, db.Model):
    __tablename__ = 'game_sketches'

    id = sqla.Column(sqla.Integer, primary_key = True)
    name = sqla.Column(sqla.String(128))
    number = sqla.Column(sqla.Integer)
    current = sqla.Column(sqla.Boolean)
    code = sqla.Column(sqla.Text)
    ext = sqla.Column(sqla.String(12))
    mode = sqla.Column(sqla.String(64))
    file_name = sqla.Column(sqla.String(128))
    file_source = sqla.Column(sqla.String(256))
    file_tab_size = sqla.Column(sqla.Integer)
    file_lines = sqla.Column(sqla.Integer)
    timestamp = sqla.Column(sqla.DateTime, index=True, default=datetime.utcnow,
                            nullable=False)
    user_code = sqla.Column(sqla.Text)
    current_line = sqla.Column(sqla.Integer, default=0)
    current_char = sqla.Column(sqla.Integer, default=0)
    # start_line = sqla.Column(sqla.Integer)
    # end_line = sqla.Column(sqla.Integer)
    ready = sqla.Column(sqla.Text)
    previous_ready = sqla.Column(sqla.Text)
    score = sqla.Column(sqla.Integer)
    difficulty = sqla.Column(sqla.String(128))

    is_done = sqla.Column(sqla.Enum('init','continue','finished'), default='init')
    is_self = sqla.Column(sqla.Boolean, default=False)
    file_game_sketch_id = sqla.Column(sqla.Integer, sqla.ForeignKey(FileGameSketch.id), index = True)
    file_game_sketches = sqla_orm.relationship('FileGameSketch', back_populates='game_sketches')
    user_id = sqla.Column(sqla.Integer, sqla.ForeignKey(User.id), index=True)
    user = sqla_orm.relationship('User', back_populates='game_sketches')


class UserGameSketchScores(Updateable, db.Model):
    __tablename__ =  "user_game_sketch_scores"

    user_id = sqla.Column(sqla.Integer, sqla.ForeignKey(User.id), primary_key = True)
    game_sketches_id = sqla.Column(sqla.Integer, sqla.ForeignKey(GameSketch.id), primary_key = True)
    score = sqla.Column(sqla.Integer)

    game_sketch = sqla_orm.relationship(GameSketch, lazy="joined")
class TemplateProjectSketch(Updateable, db.Model):
    __tablename__ = 'template_project_sketches'

    id = sqla.Column(sqla.Integer, primary_key = True)
    name = sqla.Column(sqla.String(128))
    description = sqla.Column(sqla.String(128))
    code = sqla.Column(sqla.Text)

    # game_sketches = sqla_orm.relationship('GameSketch', back_populates='project_game_sketches')
    template_file_sketches = sqla_orm.relationship('TemplateFileSketch', back_populates='template_project_sketches')

class TemplateFileSketch(Updateable, db.Model):
    __tablename__ = 'template_file_sketches'

    id = sqla.Column(sqla.Integer, primary_key = True)
    name = sqla.Column(sqla.String(64))
    code = sqla.Column(sqla.Text)
    # lines = sqla.Column(sqla.Integer)
    template_project_sketch_id = sqla.Column(sqla.Integer, sqla.ForeignKey(TemplateProjectSketch.id), index=True)
    template_project_sketches = sqla_orm.relationship('TemplateProjectSketch', back_populates='template_file_sketches')
    template_sketches = sqla_orm.relationship('TemplateSketch', back_populates='template_file_sketches')

    # def __init__(self, name, code, lines, project_project_sketches):
    #     self.name = name
    #     self.lines = lines
    #     self.code = lines * '\n'
    #     self.template_project_sketches = project_project_sketches

class TemplateSketch(Updateable, db.Model):
    __tablename__ = 'template_sketches'

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String(64))
    number = sqla.Column(sqla.Integer)
    current = sqla.Column(sqla.Boolean)
    code = sqla.Column(sqla.Text)
    ext = sqla.Column(sqla.String(12))
    mode = sqla.Column(sqla.String(64))
    file_name = sqla.Column(sqla.String(128))
    file_source = sqla.Column(sqla.String(256))
    file_tab_size = sqla.Column(sqla.Integer)
    file_lines = sqla.Column(sqla.Integer)
    timestamp = sqla.Column(sqla.DateTime, index=True, default=datetime.utcnow,
                            nullable=False)
    score = sqla.Column(sqla.Integer)
    difficulty = sqla.Column(sqla.String(128))
    ready = sqla.Column(sqla.Text)
    previous_ready = sqla.Column(sqla.Text)
    # start_line = sqla.Column(sqla.Integer)
    # end_line = sqla.Column(sqla.Integer)

    template_file_sketch_id = sqla.Column(sqla.Integer, sqla.ForeignKey(TemplateFileSketch.id), index = True)
    template_file_sketches = sqla_orm.relationship('TemplateFileSketch', back_populates='template_sketches')



    def __repr__(self):
        return '<Template Sketch {}>'.format(self.code)

    @property
    def url(self):
        return url_for('template_sketches.get', id=self.id)

class Sketch(Updateable, db.Model):
    __tablename__ = 'sketchs'

    id = sqla.Column(sqla.Integer, primary_key=True)
    code = sqla.Column(sqla.Text)
    timestamp = sqla.Column(sqla.DateTime, index=True, default=datetime.utcnow,
                            nullable=False)
    user_id = sqla.Column(sqla.Integer, sqla.ForeignKey(User.id), index=True)
    author = sqla_orm.relationship('User', back_populates='sketches')

    def __repr__(self):
        return '<Sketch {}>'.format(self.code)

    @property
    def url(self):
        return url_for('sketches.get', id=self.id)

class User_TemplateSketch(Updateable, db.Model):
    __tablename__ = 'user_template_sketches'

    id = sqla.Column(sqla.Integer, primary_key = True)
    user_id = sqla.Column(sqla.Integer, sqla.ForeignKey(User.id), primary_key = True)
    template_sketch_id = sqla.Column(sqla.Integer, sqla.ForeignKey(TemplateSketch.id), primary_key = True)
    is_done = sqla.Column(sqla.Boolean, default = False)
    user = sqla_orm.relationship("User", backref=sqla_orm.backref("user_template_sketches"))
    template_sketch = sqla_orm.relationship("TemplateSketch", backref=sqla_orm.backref("user_template_sketches"))

class Post(Updateable, db.Model):
    __tablename__ = 'posts'

    id = sqla.Column(sqla.Integer, primary_key=True)
    text = sqla.Column(sqla.String(280), nullable=False)
    timestamp = sqla.Column(sqla.DateTime, index=True, default=datetime.utcnow,
                            nullable=False)
    # user_id = sqla.Column(sqla.Integer, sqla.ForeignKey(User.id), index=True)

    # author = sqla_orm.relationship('User', back_populates='posts')

    def __repr__(self):  # pragma: no cover
        return '<Post {}>'.format(self.text)

    @property
    def url(self):
        return url_for('posts.get', id=self.id)


class Day(Updateable, db.Model):
    __tablename__ = 'day'


    id = sqla.Column(sqla.Integer, primary_key=True)
    date = sqla.Column(sqla.DateTime, nullable=False)



# class Lesson(Updateable, db.Model):
#     __tablename__ = 'lesson'

#     id = sqla.Column(sqla.Integer, primary_key=True)

#     name = sqla.Column()
#     time_start = sqla.Column()
#     time_end = sqla.Column()

# class Attend(Updateable, db.Model):
#     __tablename__ = 'attend'

#     user = sqla.ForeignKey()
#     lesson = sqla.ForeignKey()
#     status = sqla.Column()




class FileSystemNode(Updateable, db.Model):

    __tablename__ = 'file_system_nodes'

    id = sqla.Column(sqla.Integer, primary_key=True)
    # uuid = sqla.Column(sqla.String)
    name = sqla.Column(sqla.String, nullable=False)
    content = sqla.Column(sqla.Text)
    is_hidden = sqla.Column(sqla.Boolean)
    
    is_folder = sqla.Column(sqla.Boolean)

    parent_folder_id = sqla.Column(
        sqla.Integer,
        sqla.ForeignKey("file_system_nodes.id", ondelete="CASCADE", onupdate="CASCADE"),
        comment="When parent folder is NULL, is root folder")

    user_id = sqla.Column(sqla.Integer, sqla.ForeignKey(User.id), index=True)
    user = sqla_orm.relationship('User', back_populates='file_system_nodes')


class Packages(Updateable, db.Model):

    __tablename__ = 'packages'

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String)
    path = sqla.Column(sqla.String)


class Level(Updateable, db.Model):

    __tablename__ = 'level'

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String)
    xp = sqla.Column(sqla.Integer)



class Project(Updateable, db.Model):

    __tablename__ = 'project'

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String)
    episodes = sqla_orm.relationship('Episode', back_populates='project')

# class GameApplication(Updateable, db.Model):

#     __tablename__ = 'game_application'

#     id = sqla.Column(sqla.Integer, primary_key=True)
#     name = sqla.Column(sqla.String)
#     description = sqla.Column(sqla.String)
#     episodes = sqla_orm.relationship('Episode', back_populates='application')
#     completed = sqla #

#     # files = sqla_orm.relationship("Files", back_populates="application")

#     def episode_select(self):
#          return Episode.select().where(sqla_orm.with_parent(self, Application.episodes))
class Application(Updateable, db.Model):

    __tablename__ = 'application'

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String, unique=True)
    description = sqla.Column(sqla.String)
    path = sqla.Column(sqla.String)
    episodes = sqla_orm.relationship('Episode', back_populates='application', cascade="all, delete-orphan")
    user = sqla_orm.relationship("ApplicationUserLink", back_populates="application", cascade="all, delete-orphan")

    files = sqla_orm.relationship("Files", back_populates="application")

    def episode_select(self):
         return Episode.select().where(sqla_orm.with_parent(self, Application.episodes))
class Episode(Updateable, db.Model):
    
    __tablename__ = 'episode'

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String, unique=True)
    project_id = sqla.Column(sqla.ForeignKey(Project.id), index=True)
    project= sqla_orm.relationship("Project", back_populates="episodes")
    lines = sqla_orm.relationship('Lines', back_populates="episodes",  cascade="all, delete-orphan")
    application = sqla_orm.relationship("Application", back_populates="episodes")
    application_id = sqla.Column(sqla.ForeignKey(Application.id), index=True)
    path = sqla.Column(sqla.String)
    files = sqla_orm.relationship("Files", back_populates="episode",  cascade="all, delete-orphan")
    user = sqla_orm.relationship("EpisodeUserLink", back_populates="episode", cascade="all, delete-orphan")

    def files_select(self):
         return Files.select().where(sqla_orm.with_parent(self, Episode.files))

    def lines_select(self):
        return Lines.select().where(sqla_orm.with_parent(self, Episode.lines))

class Files(Updateable, db.Model):

    __tablename__ = 'files'

    id = sqla.Column(sqla.Integer, primary_key=True)
    # code = sqla.Column(sqla.Text)
    path = sqla.Column(sqla.String)
    name = sqla.Column(sqla.String)
    # lines = sqla_orm.relationship('Lines', back_populates="files")
    # difference = sqla.Column(sqla.String)
    application_id = sqla.Column(sqla.ForeignKey(Application.id), index=True)
    application = sqla_orm.relationship("Application", back_populates="files")
    episode_id = sqla.Column(sqla.ForeignKey(Episode.id), index=True)
    episode = sqla_orm.relationship("Episode", back_populates="files")


    # @hybrid_method
    # def difference(self, other):
    #     current,target = '',''
    #     with open(other.path) as f:
    #         current = f.read()
    #     with open(self.path) as f:
    #         target = f.read()
    #     current = current.splitlines(keepends=True)
    #     target = target.splitlines(keepends=True)
    #     diff = list(difflib.ndiff(current, target))
    #     lines = []
    #     for i in diff:
    #         if i[0] == '+':
    #             lines.append(i[1:])
    #     return lines

    # @difference.expression
    # def difference(self, other):
    #     return self.difference(self, other)

    def read_for_split(self):
        import os
        with open(os.path.join(os.getcwd(),'uploads/applications/' + self.episode.application.path + '/' + self.episode.path + '/' + self.path)) as f:
            lines = f.read()
            return lines.splitlines(keepends=True)
    def read(self):
        import os
        with open(os.path.join(os.getcwd(),'uploads/applications/' + self.episode.application.path + '/' + self.episode.path + '/' + self.path)) as f:
            lines = f.readlines()
            return ''.join(lines)
class Lines(Updateable, db.Model):

    __tablename = 'lines'

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String(64))
    number = sqla.Column(sqla.Integer)
    code = sqla.Column(sqla.Text)
    ext = sqla.Column(sqla.String(12))
    mode = sqla.Column(sqla.String(64))
    file_name = sqla.Column(sqla.String(128))
    file_source = sqla.Column(sqla.String(256))
    file_tab_size = sqla.Column(sqla.Integer)
    file_lines = sqla.Column(sqla.Integer)
    timestamp = sqla.Column(sqla.DateTime, index=True, default=datetime.utcnow,
                            nullable=False)
    score = sqla.Column(sqla.Integer)
    difficulty = sqla.Column(sqla.String(128))


    # file_id = sqla.Column(sqla.ForeignKey(Files.id), index=True)
    # files = sqla_orm.relationship("Files", back_populates="lines")
    episode_id = sqla.Column(sqla.ForeignKey(Episode.id), index=True)
    episodes = sqla_orm.relationship("Episode", back_populates="lines")
    user = sqla_orm.relationship("LinesUserLink", back_populates="lines", cascade="all, delete-orphan")


class GameApplication(Updateable, db.Model):

    __tablename__ = 'game_application'

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String, unique=True)
    description = sqla.Column(sqla.String)
    path = sqla.Column(sqla.String)
    game_episodes = sqla_orm.relationship('GameEpisode', back_populates='game_application', cascade="all, delete-orphan")
    is_finished = sqla.Column(sqla.Boolean, default=False)
    user_id = sqla.Column(sqla.Integer, sqla.ForeignKey(User.id), index=True)
    user = sqla_orm.relationship('User', back_populates='game_application')

    def episode_select(self):
         return Episode.select().where(sqla_orm.with_parent(self, Application.episodes))


class GameEpisode(Updateable, db.Model):

    __tablename__ = 'game_episode'

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String, unique=True)
    is_finished = sqla.Column(sqla.Boolean)
    game_files = sqla_orm.relationship('GameFiles', back_populates="game_episodes", cascade="all, delete-orphan")
    game_lines = sqla_orm.relationship('GameLines', back_populates="game_episodes",  cascade="all, delete-orphan")
    game_application = sqla_orm.relationship("GameApplication", back_populates="game_episodes")
    game_application_id = sqla.Column(sqla.ForeignKey(GameApplication.id), index=True)
    path = sqla.Column(sqla.String)
    code = sqla.Column(sqla.String)


    def game_files_select(self):
         return GameFiles.select().where(sqla_orm.with_parent(self, GameEpisode.game_files))

    def game_lines_select(self):
        return GameLines.select().where(sqla_orm.with_parent(self, GameEpisode.game_lines))

class GameFiles(Updateable, db.Model):

    __tablename__ = 'game_files'

    id = sqla.Column(sqla.Integer, primary_key=True)
    path = sqla.Column(sqla.String)
    name = sqla.Column(sqla.String)
    game_episodes_id = sqla.Column(sqla.ForeignKey(GameEpisode.id), index=True)
    game_episodes = sqla_orm.relationship("GameEpisode", back_populates="game_files")


    def read_for_split(self):
        import os
        with open(os.path.join(os.getcwd(),'uploads/applications/' + self.game_episodes.game_application.path + '/' + self.game_episodes.path + '/' + self.path)) as f:
            lines = f.read()
            return lines.splitlines(keepends=True)


    def read(self):
        import os
        with open(os.path.join(os.getcwd(),'uploads/applications/' + self.game_episodes.game_application.path + '/' + self.game_episodes.path + '/' + self.path)) as f:
            lines = f.readlines()
            return ''.join(lines)


class GameLines(Updateable, db.Model):

    __tablename__ = 'game_lines'


    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String(64))
    number = sqla.Column(sqla.Integer)
    current = sqla.Column(sqla.Boolean)
    code = sqla.Column(sqla.Text)
    ext = sqla.Column(sqla.String(12))
    mode = sqla.Column(sqla.String(64))
    file_name = sqla.Column(sqla.String(128))
    file_source = sqla.Column(sqla.String(256))
    file_tab_size = sqla.Column(sqla.Integer)
    file_lines = sqla.Column(sqla.Integer)
    timestamp = sqla.Column(sqla.DateTime, index=True, default=datetime.utcnow,
                            nullable=False)
    score = sqla.Column(sqla.Integer)
    difficulty = sqla.Column(sqla.String(128))
    state = sqla.Column(sqla.Enum('init','continue','finished'), default='init')
    current_line = sqla.Column(sqla.Integer, default=0)
    current_char = sqla.Column(sqla.Integer, default=0)
    game_episodes_id = sqla.Column(sqla.Integer, sqla.ForeignKey(GameEpisode.id), index=True)
    game_episodes = sqla_orm.relationship("GameEpisode", back_populates="game_lines")


class ApplicationUserLink(Updateable, db.Model):
    __tablename__ = 'application_user_link'

    user_id = sqla.Column(sqla.Integer, sqla.ForeignKey(User.id), primary_key=True)
    application_id = sqla.Column(sqla.Integer, sqla.ForeignKey(Application.id), primary_key=True)

    is_finished = sqla.Column(sqla.Boolean, default=False)

    application = sqla_orm.relationship("Application", back_populates="user")
    user = sqla_orm.relationship("User", back_populates="application")

class EpisodeUserLink(Updateable, db.Model):
    __tablename__ = 'episode_user_link'

    user_id = sqla.Column(sqla.Integer, sqla.ForeignKey(User.id), primary_key=True)
    episode_id = sqla.Column(sqla.Integer, sqla.ForeignKey(Episode.id), primary_key=True)

    is_finished = sqla.Column(sqla.Boolean, default=False)

    episode = sqla_orm.relationship("Episode", back_populates="user")
    user = sqla_orm.relationship("User", back_populates="episode")

class LinesUserLink(Updateable, db.Model):
    __tablename__ = 'lines_user_link'

    
    user_id = sqla.Column(sqla.Integer, sqla.ForeignKey(User.id), primary_key=True)
    lines_id = sqla.Column(sqla.Integer, sqla.ForeignKey(Lines.id), primary_key=True)

    is_finished = sqla.Column(sqla.Boolean, default=False)
    state = sqla.Column(sqla.Enum('init','continue','finished'), default='init')
    current = sqla.Column(sqla.Boolean, default=False)
    current_line = sqla.Column(sqla.Integer, default=0)
    current_char = sqla.Column(sqla.Integer, default=0)

    lines = sqla_orm.relationship("Lines", back_populates="user")
    user = sqla_orm.relationship("User", back_populates="lines")