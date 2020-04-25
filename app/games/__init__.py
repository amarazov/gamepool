from flask import Blueprint

bp = Blueprint('games', __name__)

from app.games import routes
