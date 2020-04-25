from flask import request, session as sess
from flask_login import login_required, current_user

from app import db
from app.games.arithmetic import bp
from app.models import Answer, Game, Attempt


@bp.route('/games/_post_answer/', methods=['GET', 'POST'])
@login_required
def post_answer():
    if request.method == 'POST':
        data = request.get_json()
        game_name = data['game_name']
        typ = data['game_typ']
        print(game_name, typ)
        del data['game_name'], data['game_typ']
        game = Game.query.filter_by(name=game_name, typ=typ).first()

        if 'answer_id' in data:
            answer = Answer.query.filter_by(id=data['answer_id']).first()
        else:
            answer = Answer()
            answer.user_id = current_user.id
            if sess['session_id'] > 0 and 'attempt_id' in sess:
                t = Attempt.query.get(sess['attempt_id'])
                t.answers.append(answer)
            else:
                db.session.add(answer)
        answer.game_id = game.id
        for attr in data:
            setattr(answer, attr, data[attr])
        db.session.commit()
        if 'progress' in sess:
            sess['progress'] += 1
        return ""
    else:
        pass
