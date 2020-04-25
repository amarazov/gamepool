import json
import random

from flask import render_template, jsonify, session as sess
from flask_login import login_required

from app.games.arithmetic import bp
from app.models import Game


@bp.route('/games/_arithmetic.game/', methods=['GET', 'POST'])
@login_required
def game_data():
    game_name = 'arithmetic.game'
    typ = sess.pop('game.typ', '*')
    game = Game.query.filter_by(name=game_name, typ=typ).first().eval
    args = json.loads(str(game.args))
    ops = dict(minus='-', plus='+', mult='*')
    op = ops[game.typ.split(".")[0]]
    choices = set()
    while len(choices) < 4:
        arg1 = random.randint(*args['arg1'])
        arg2 = random.randint(*args['arg2'])
        res = eval('{}{}{}'.format(arg1, op, arg2))
        if args['res'][0] <= res <= args['res'][1]:
            choices.add(res)
    choices = list(choices)
    random.shuffle(choices)

    return jsonify(dict(game_typ=typ, args=dict(a=arg1, op=op, b=arg2, res=res, choices=choices)))


@bp.route('/games/arithmetic.game/<typ>/<is_session>/', )
@login_required
def game(typ, is_session):
    if is_session != 'True':
        sess['last.game.name'] = 'arithmetic.game'
        sess['last.game.typ'] = typ
        sess['session_id'] = -1
    return render_template('arithmetic.game.html', typ=typ)
