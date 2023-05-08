from flask import Flask, redirect, url_for, request
from alchemical.flask import Alchemical
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_mail import Mail
from apifairy import APIFairy
from config import Config

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = Alchemical()
migrate = Migrate()
ma = Marshmallow()
cors = CORS()
mail = Mail()
apifairy = APIFairy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # extensions
    from api import models
    db.init_app(app)
    # db.create_all()
    migrate.init_app(app, db)
    ma.init_app(app)
    if app.config['USE_CORS']:  # pragma: no branch
        cors.init_app(app)
    mail.init_app(app)
    apifairy.init_app(app)

    # blueprints
    from api.errors import errors
    app.register_blueprint(errors)
    from api.tokens import tokens
    app.register_blueprint(tokens, url_prefix='/api')
    from api.users import users
    app.register_blueprint(users, url_prefix='/api')
    from api.sketches import sketches
    app.register_blueprint(sketches, url_prefix='/api')
    from api.template_sketches import template_sketches
    app.register_blueprint(template_sketches, url_prefix='/api')
    from api.project_game_sketches import project_game_sketches
    app.register_blueprint(project_game_sketches, url_prefix='/api')
    from api.file_game_sketches import file_game_sketches
    app.register_blueprint(file_game_sketches, url_prefix='/api')
    from api.game_sketches import game_sketches
    app.register_blueprint(game_sketches, url_prefix='/api')
    from api.day import day
    app.register_blueprint(day, url_prefix='/api')
    from api.file_system_node import file_system_nodes
    app.register_blueprint(file_system_nodes, url_prefix='/api')
    from api.packages import packages
    app.register_blueprint(packages, url_prefix='/api')
    from api.files import files
    app.register_blueprint(files, url_prefix='/api')
    from api.application import application
    app.register_blueprint(application, url_prefix='/api')
    from api.episode import episode
    app.register_blueprint(episode, url_prefix='/api')
    from api.lines import lines
    app.register_blueprint(lines, url_prefix='/api')
    from api.fake import fake
    app.register_blueprint(fake)
    from api.test import test
    app.register_blueprint(test)

    # define the shell context
    @app.shell_context_processor
    def shell_context():  # pragma: no cover
        ctx = {'db': db}
        for attr in dir(models):
            model = getattr(models, attr)
            if hasattr(model, '__bases__') and \
                    db.Model in getattr(model, '__bases__'):
                ctx[attr] = model
        return ctx

    @app.route('/')
    def index():  # pragma: no cover
        return redirect(url_for('apifairy.docs'))


    @app.after_request
    def after_request(response):
        # Werkzeu sometimes does not flush the request body so we do it here
        request.get_data()
        return response

    return app
