from flask import Blueprint

bp = Blueprint('games.simonsays', __name__, template_folder='templates', static_folder='static', static_url_path='/static/games.simonsays')

from app.games.simonsays import routes
