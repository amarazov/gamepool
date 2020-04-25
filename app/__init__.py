import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, request, current_app, session as sess, g
from flask_babel import Babel
from flask_babel import lazy_gettext as _l
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.games import bp as games_bp
    app.register_blueprint(games_bp)

    from app.games.arithmetic import bp as arithmetic_bp
    app.register_blueprint(arithmetic_bp)

    from app.games.memory_tiles import bp as memory_tiles_bp
    app.register_blueprint(memory_tiles_bp)

    from app.games.simonsays import bp as simonsays_bp
    app.register_blueprint(simonsays_bp)

    from app.games.fiteensliding import bp as fiteensliding_bp
    app.register_blueprint(fiteensliding_bp)

    from app.games.picturesliding import bp as picturesliding_bp
    app.register_blueprint(picturesliding_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/gamepool.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('gamepool startup')

    return app


@babel.localeselector
def get_locale():
    # if request.args.get('lang'):
    #     return request.accept_languages.best_match([request.args.get('lang')])
    # return request.accept_languages.best_match(current_app.config['LANGUAGES'])
    return 'bg'


