from flask import Blueprint

bp = Blueprint('auth', __name__, template_folder='templates')

ACCESS = {
    'guest': 0,
    'user': 10,
    'admin': 20
}

from app.auth import routes
