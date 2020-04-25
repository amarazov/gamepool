from flask import render_template, session as sess
from flask_login import login_required

from app.games.picturesliding import bp
from app.models import Game


@bp.route('/games/picturesliding.game/<typ>/<is_session>/', )
@login_required
def game(typ, is_session):
    if is_session != 'True':
        sess['last.game.name'] = 'picturesliding.game'
        sess['last.game.typ'] = typ
        sess['session_id'] = -1
    game = Game.query.filter_by(name='picturesliding.game', typ=typ).first().eval
    return render_template('picturesliding.game.html', typ=game.typ)
