from marshmallow import validate, validates, validates_schema, \
    ValidationError, post_dump
from api import ma, db
from api.auth import token_auth
from api.models import Files, GameSketch, User, Post, Sketch, TemplateSketch, ProjectGameSketch, FileGameSketch, Day, FileSystemNode, Packages, \
    Application, Episode, Lines, ApplicationUserLink, EpisodeUserLink, LinesUserLink
from apifairy.fields import FileField

paginated_schema_cache = {}


class EmptySchema(ma.Schema):
    pass


class DateTimePaginationSchema(ma.Schema):
    class Meta:
        ordered = True

    limit = ma.Integer()
    offset = ma.Integer()
    after = ma.DateTime(load_only=True)
    count = ma.Integer(dump_only=True)
    total = ma.Integer(dump_only=True)

    @validates_schema
    def validate_schema(self, data, **kwargs):
        if data.get('offset') is not None and data.get('after') is not None:
            raise ValidationError('Cannot specify both offset and after')


class StringPaginationSchema(ma.Schema):
    class Meta:
        ordered = True

    limit = ma.Integer()
    offset = ma.Integer()
    after = ma.String(load_only=True)
    count = ma.Integer(dump_only=True)
    total = ma.Integer(dump_only=True)

    @validates_schema
    def validate_schema(self, data, **kwargs):
        if data.get('offset') is not None and data.get('after') is not None:
            raise ValidationError('Cannot specify both offset and after')


def PaginatedCollection(schema, pagination_schema=StringPaginationSchema):
    if schema in paginated_schema_cache:
        return paginated_schema_cache[schema]

    class PaginatedSchema(ma.Schema):
        class Meta:
            ordered = True

        pagination = ma.Nested(pagination_schema)
        data = ma.Nested(schema, many=True)

    PaginatedSchema.__name__ = 'Paginated{}'.format(schema.__class__.__name__)
    paginated_schema_cache[schema] = PaginatedSchema
    return PaginatedSchema

class ApplicationFileNameSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Files

    name = ma.auto_field()
    path = ma.auto_field()

class FilesUserSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Files

    id = ma.auto_field(dump_only=True)
    path = ma.auto_field(dump_only=True)
    name = ma.auto_field(dump_only=True)
class ApplicationNameSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Application

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(dump_only=True)
    description = ma.auto_field(dump_only=True)
    # files = ma.Nested(FilesUserSchema, dump_only=True)
    episode_url = ma.URLFor('users.episode_all', values={'app_id': '<id>'},
                            dump_only=True)
class ApplicationUserLinkSchema(ma.SQLAlchemySchema):

    class Meta:
        model = ApplicationUserLink

    application = ma.Nested(ApplicationNameSchema)

    is_finished = ma.auto_field(dump_only=True)
class LinesSchema(ma.SQLAlchemySchema):


    class Meta:
        model = Lines

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field()
    number = ma.auto_field()
    code = ma.auto_field()
    ext = ma.auto_field()
    mode = ma.auto_field()
    file_name = ma.auto_field()
    file_source = ma.auto_field()
    file_tab_size = ma.auto_field()
    file_lines = ma.auto_field()
    score = ma.auto_field()
    user = ma.auto_field()

class LinesUserLinkSchema(ma.SQLAlchemySchema):

    class Meta:
        model = LinesUserLink

    lines = ma.Nested(LinesSchema)

    is_finished = ma.auto_field(dump_only=True)
    state = ma.auto_field(dump_only=True)
    current_line = ma.auto_field(dump_only=True)
    current = ma.auto_field(dump_only=True)
    current_char = ma.auto_field(dump_only=True)
class EpisodeNameSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Episode

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(dump_only=True)
    lines_url = ma.URLFor('users.lines_all', values={'ep_id': '<id>'},
                            dump_only=True)
class EpisodeUserLinkSchema(ma.SQLAlchemySchema):

    class Meta:
        model = EpisodeUserLink

    episode = ma.Nested(EpisodeNameSchema)
    is_finished = ma.auto_field(dump_only=True)

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        ordered = True

    id = ma.auto_field(dump_only=True)
    url = ma.String(dump_only=True)
    username = ma.auto_field(required=True,
                             validate=validate.Length(min=3, max=64))
    email = ma.auto_field(validate=[validate.Length(max=120),
                                                   validate.Email()])
    nickname = ma.auto_field(required=True, validate=validate.Length(min=3,max=128))
    password = ma.String(required=True, load_only=True,
                         validate=validate.Length(min=3))
    avatar_url = ma.String(dump_only=True)
    about_me = ma.auto_field()
    first_seen = ma.auto_field(dump_only=True)
    last_seen = ma.auto_field(dump_only=True)
    _total_xp = ma.auto_field(dump_only=True)
    application = ma.Nested(ApplicationUserLinkSchema, many=True, only=('application', 'is_finished'))
    lines = ma.Nested(LinesUserLinkSchema, many=True)
    # posts_url = ma.URLFor('posts.user_all', values={'id': '<id>'},
    #                       dump_only=True)
    game_sketch_url = ma.URLFor('game_sketches.user_all', values={'id': '<id>'},
                            dump_only=True)

    @validates('username')
    def validate_username(self, value):
        if not value[0].isalpha():
            raise ValidationError('Username must start with a letter')
        user = token_auth.current_user()
        old_username = user.username if user else None
        if value != old_username and \
                db.session.scalar(User.select().filter_by(username=value)):
            raise ValidationError('Используйте другое имя.')


    @validates('nickname')
    def validate_nickname(self, value):
        # if not value[0].isalpha():
        #     raise ValidationError('Username must start with a letter')
        user = token_auth.current_user()
        old_username = user.username if user else None
        if value != old_username and \
                db.session.scalar(User.select().filter_by(username=value)):
            raise ValidationError('Используйте другой никнейм.')

    @post_dump
    def fix_datetimes(self, data, **kwargs):
        data['first_seen'] += 'Z'
        data['last_seen'] += 'Z'
        return data

class UpdateUserSchema(UserSchema):
    old_password = ma.String(load_only=True, validate=validate.Length(min=3))

    @validates('old_password')
    def validate_old_password(self, value):
        if not token_auth.current_user().verify_password(value):
            raise ValidationError('Password is incorrect')

class UpdateLinesUserLinkSchema(ma.SQLAlchemySchema):

    class Meta:
        model = LinesUserLink
    id = ma.String()
    state = ma.auto_field()
    current_line = ma.auto_field()
    current = ma.auto_field()
    current_char = ma.auto_field()
class PostSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Post
        include_fk = True
        ordered = True

    id = ma.auto_field(dump_only=True)
    url = ma.String(dump_only=True)
    text = ma.auto_field(required=True, validate=validate.Length(
        min=1, max=280))
    timestamp = ma.auto_field(dump_only=True)
    # author = ma.Nested(UserSchema, dump_only=True)

    @post_dump
    def fix_datetimes(self, data, **kwargs):
        data['timestamp'] += 'Z'
        return data

class SketchSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Sketch
        include_fk = True
        ordered = True

    id = ma.auto_field(dump_only=True)
    url = ma.String(dump_only=True)
    code = ma.auto_field()
    timestamp = ma.auto_field(dump_only=True)
    author = ma.Nested(UserSchema, dump_only=True)

    @post_dump
    def fix_datetimes(self, data, **kwargs):
        data['timestamp'] += 'Z'
        return data
class GameSketchSchema(ma.SQLAlchemySchema):

    class Meta:
        model = GameSketch
        ordered = True


    id = ma.auto_field(dump_only=True)
    name = ma.auto_field()
    current = ma.auto_field()
    number = ma.auto_field()
    url = ma.String(dump_only=True)
    ext = ma.auto_field()
    mode = ma.auto_field()
    code = ma.auto_field()
    file_name = ma.auto_field()
    file_source = ma.auto_field()
    file_tab_size = ma.auto_field()
    file_lines = ma.auto_field()
    timestamp = ma.auto_field(dump_only=True)
    current_line = ma.auto_field()
    current_char = ma.auto_field()
    ready = ma.auto_field()
    previous_ready = ma.auto_field()
    user_code = ma.auto_field()
    is_done = ma.auto_field()
    is_self = ma.auto_field()
    score = ma.auto_field()
    difficulty = ma.auto_field()
    # author = ma.Nested(UserSchema, dump_only=True)
    file_game_sketch_id = ma.auto_field()

    @post_dump
    def fix_datetimes(self, data, **kwargs):
        data['timestamp'] += 'Z'
        return data

class FileGameSketchSchema(ma.SQLAlchemySchema):

    class Meta:
        model = FileGameSketch
        ordered = True

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field()
    code = ma.auto_field()
    previous_code = ma.auto_field()
    is_done = ma.auto_field()
    timestamp = ma.auto_field(dump_only=True)
    project_game_sketch_id = ma.auto_field(dump_only=True)
    game_sketches = ma.List(ma.Nested(GameSketchSchema))
    # game_sketches_url = ma.URLFor('game_sketches.user_all', values={'id': '<id>'}, dump_only=True)
    # game_sketch_url = ma.URLFor('game_sketches.user_all', values={'id': '<id>'},
    #                         dump_only=True)

    @post_dump
    def fix_datetimes(self, data, **kwargs):
        data['timestamp'] += 'Z'
        return data
class ProjectGameSketchSchema(ma.SQLAlchemySchema):

    class Meta:
        model = ProjectGameSketch
        ordered = True


    id = ma.auto_field(dump_only=True)
    name = ma.auto_field()
    description = ma.auto_field(dump_only=True)
    is_done = ma.auto_field()
    timestamp = ma.auto_field(dump_only=True)
    path = ma.auto_field()
    author = ma.Nested(UserSchema, dump_only=True)
    file_game_sketches = ma.List(ma.Nested(FileGameSketchSchema, dump_only=True))

    @post_dump
    def fix_datetimes(self, data, **kwargs):
        data['timestamp'] += 'Z'
        return data
class TemplateSketchSchema(ma.SQLAlchemySchema):

    class Meta:
        model = TemplateSketch
        ordered = True

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field()
    url = ma.String(dump_only=True)
    ext = ma.auto_field()
    mode = ma.auto_field()
    code = ma.auto_field()
    file_name = ma.auto_field()
    file_source = ma.auto_field()
    file_tab_size = ma.auto_field()
    file_lines = ma.auto_field()
    ready = ma.auto_field()
    timestamp = ma.auto_field(dump_only=True)
    score = ma.auto_field()
    difficulty = ma.auto_field()

    @post_dump
    def fix_datetimes(self, data, **kwargs):
        data['timestamp'] += 'Z'
        return data

class TokenSchema(ma.Schema):
    class Meta:
        ordered = True

    access_token = ma.String(required=True)
    user = ma.Nested(UserSchema, dump_only=True)
    refresh_token = ma.String()


class PasswordResetRequestSchema(ma.Schema):
    class Meta:
        ordered = True

    email = ma.String(required=True, validate=[validate.Length(max=120),
                                               validate.Email()])


class PasswordResetSchema(ma.Schema):
    class Meta:
        ordered = True

    token = ma.String(required=True)
    new_password = ma.String(required=True, validate=validate.Length(min=3))


class DaySchema(ma.SQLAlchemySchema):
    
    class Meta:
        model = Day

    count_month = ma.String(required=True)
    day_in_week = ma.String(required=True)


class FileSystemNodeSchema(ma.SQLAlchemySchema):


    class Meta:
        model = FileSystemNode

    id = ma.auto_field(dump_only=True)
    # uuid = ma.auto_field()
    name = ma.auto_field()
    is_folder = ma.auto_field()
    content = ma.auto_field()
    parent_folder_id = ma.auto_field()


class UpdateFileSystemNodeSchema(FileSystemNodeSchema):
    name = ma.String(load_only=True)


class PackagesSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Packages

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field()
    path = ma.auto_field()
    wheel = FileField()

class IdSchema(ma.SQLAlchemySchema):

    ids = ma.List(ma.Integer())
class UserNameSchema(ma.SQLAlchemySchema):

    class Meta:
        model = User

    username = ma.auto_field()


class ApplicationUserNameLinkSchema(ma.SQLAlchemySchema):

    class Meta:
        model = ApplicationUserLink

    user = ma.auto_field()

    is_finished = ma.auto_field()

class ApplicationSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Application

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field()
    path = ma.auto_field()
    description = ma.auto_field()
    user = ma.Nested(ApplicationUserNameLinkSchema, many=True, only=('user', 'is_finished'))
    files = ma.Nested(ApplicationFileNameSchema, dump_only=True, many=True)


class FileNameSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Files

    name = ma.auto_field()
    path = ma.auto_field()
    
class LinesNameSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Lines

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(dump_only=True)


class EpisodeSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Episode
        # include_fk = True
    
    id = ma.auto_field(dump_only=True)
    name = ma.auto_field()
    path = ma.auto_field()  
    files = ma.Nested(FileNameSchema, dump_only=True, many=True)
    lines = ma.Nested(LinesNameSchema, dump_only=True, many=True)

    

class ApplicationFilesSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Files

    id = ma.auto_field(dump_only=True)
    path = ma.auto_field(dump_only=True)
    name = ma.auto_field(dump_only=True)
    files = FileField()
class FilesSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Files

    id = ma.auto_field(dump_only=True)
    path = ma.auto_field(dump_only=True)
    name = ma.auto_field(dump_only=True)
    py = FileField()

class UpdateFilesSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Files
    
    name = ma.auto_field()
class FilesCodeSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Files

    id = ma.auto_field(dump_only=True)
    path = ma.auto_field(dump_only=True)
    name = ma.auto_field(dump_only=True)
    files = ma.String(dump_only=True)
    code = ma.Function(lambda obj: obj.read())
    split = ma.Function(lambda obj: obj.read_for_split())


    

class DataLineSchema(ma.SQLAlchemySchema):

    objects = ma.Nested(LinesSchema)