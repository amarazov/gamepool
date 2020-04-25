from flask import Blueprint

bp = Blueprint('games.picturesliding', __name__, template_folder='templates', static_folder='static',
               static_url_path='/static/games.picturesliding')

from app.games.picturesliding import routes
