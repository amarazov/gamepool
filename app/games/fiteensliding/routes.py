from flask import render_template, session as sess
from flask_login import login_required

from app.games.fiteensliding import bp


@bp.route('/games/fiteensliding.game/<typ>/<is_session>/', )
@login_required
def game(typ, is_session):
    if is_session != 'True':
        sess['last.game.name'] = 'fiteensliding.game'
        sess['last.game.typ'] = typ
        sess['session_id'] = -1
    return render_template('fiteensliding_game.html', typ=typ)
