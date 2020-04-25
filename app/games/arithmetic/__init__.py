from flask import Blueprint

bp = Blueprint('games.arithmetic', __name__, template_folder='templates', static_folder='static')

from app.games.arithmetic import routes
