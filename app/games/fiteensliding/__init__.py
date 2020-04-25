from flask import Blueprint

bp = Blueprint('games.fiteensliding', __name__, template_folder='templates', static_folder='static',
               static_url_path='/static/games.fiteensliding')

from app.games.fiteensliding import routes
