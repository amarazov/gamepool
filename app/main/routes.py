from datetime import datetime

from flask import render_template, g, url_for, redirect, session as sess
from flask_babel import get_locale, lazy_gettext as _l
from flask_login import current_user, login_required

from app import db
from app.main import bp
from app.models import User, Session, Attempt


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    games = db.engine.execute('select distinct name from game')
    game_urls = []
    for game_name in games:
        game_name = game_name[0]
        game_urls.append((url_for('games.' + game_name, typ='*', is_session=False), game_name))
    return render_template('index.html', title=_l('Home'), game_urls=game_urls)


@bp.route('/start_session/')
@login_required
def start_session():
    if current_user.sessions:
        sess['session_id'] = current_user.sessions[-1].id
    else:
        return render_template('no_session.html', title=_l('No Session'))
    return next_game()


@bp.route('/stop_session/')
@login_required
def stop_session():
    sess.pop('session_id', None)
    sess.pop('attempt_id', None)
    sess.pop('progress', None)
    return redirect(url_for('main.finished_session'))


@bp.route('/next_game/')
@login_required
def next_game():
    if 'session_id' not in sess or sess['session_id'] < 0:
        return redirect(url_for('games.' + sess['last.game.name'], typ=sess['last.game.typ'], is_session=False))
    session_id = sess['session_id']
    s = Session.query.get(session_id)
    if 'attempt_id' not in sess:
        a = Attempt(session_id=session_id, user_id=current_user.id)
        s.attempts.append(a)
        db.session().commit()
        sess['attempt_id'] = a.id
        sess['progress'] = 0
    try:
        game = s.games[sess['progress']].eval
        return redirect(url_for('games.' + game.name, typ=game.typ, is_session=True))
    except IndexError:
        # Deactivate session
        return stop_session()


@bp.route('/finished_session/')
@login_required
def finished_session():
    return render_template('finished_session.html')


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)
