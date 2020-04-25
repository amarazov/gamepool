from flask import render_template, session as sess
from flask_login import login_required

from app.games.simonsays import bp


@bp.route('/games/simonsays.game/<typ>/<is_session>/')
@login_required
def game(typ, is_session):
    if is_session != 'True':
        sess['last.game.name'] = 'simonsays.game'
        sess['last.game.typ'] = typ
        sess['session_id'] = -1
    return render_template('simonsays.game.html', typ=typ)
