from flask import render_template, session as sess
from flask_login import login_required

from app.games.memory_tiles import bp


@bp.route('/games/memory_tiles.game/<typ>/<is_session>/', )
@login_required
def game(typ, is_session):
    if is_session != 'True':
        sess['last.game.name'] = 'memory_tiles.game'
        sess['last.game.typ'] = typ
        sess['session_id'] = -1
    try:
        typ = int(typ)
        if typ < 0 or typ > 12:
            raise ValueError()
    except ValueError:
        typ = 12
    return render_template('memory_tiles.game.html', typ=typ)
