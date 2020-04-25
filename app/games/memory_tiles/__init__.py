from flask import Blueprint

bp = Blueprint('games.memory_tiles', __name__, template_folder='templates', static_folder='static', static_url_path='/static/games.memory_tiles')

from app.games.memory_tiles import routes
