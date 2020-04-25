from functools import wraps

import jwt
from flask import render_template, flash, redirect, url_for, request, session as sess, current_app
from flask_babel import lazy_gettext as _l
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app import db
from app.auth import bp, ACCESS
from app.auth.email import send_password_reset_email
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordForm, LabelRequestForm, \
    AssignUserToSessionRequestForm
from app.auth.forms import ResetPasswordRequestForm
from app.models import User, Session


def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not sess.get('user_id'):
                return redirect(url_for('auth.login'))
            user = User.query.get(sess.get('user_id'))
            if not user.allowed(access_level):
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_l('Invalid username or password'))
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', title=_l('Sign In'), form=form)


@bp.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.set_label(form.token.data)
        db.session.add(user)
        db.session.commit()
        flash(_l('Congratulations, you are now a registered user!'))
        return redirect(url_for('auth.login'))
    return render_template('register.html', title=_l('Register'), form=form)


@bp.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/reset_password_request/', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(_l('Check your email for the instructions to reset your password'))
        return redirect(url_for('auth.login'))
    return render_template('reset_password_request.html',
                           title=_l('Reset Password'), form=form)


@bp.route('/reset_password/<token>/', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_l('Your password has been reset.'))
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form)


def generate_label(label):
    return jwt.encode({'label': label},
        current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')


@bp.route('/get_label_request/', methods=['GET', 'POST'])
@requires_access_level(access_level=ACCESS['admin'])
def get_label_request():
    form = LabelRequestForm()
    if form.validate_on_submit():
        label = form.label.data
        if not label:
            flash(_l('Invalid label'))
            return redirect(url_for('auth.get_label_request'))
        token = generate_label(label)
        return render_template('get_label.html', token=token)
    return render_template('get_label_form.html', title=_l('Patient Label'), form=form)


@bp.route('/add_session_request/', methods=['GET', 'POST'])
@requires_access_level(access_level=ACCESS['admin'])
def add_session_request():
    form = AssignUserToSessionRequestForm()
    if form.validate_on_submit():
        label = form.label.data
        session_name = form.session_name.data
        u = User.query.filter_by(label=label).first()
        s = Session.query.filter_by(name=session_name).first()
        u.sessions.append(s)
        db.session().commit()
        return render_template('assign_session.html', title=_l('Assign session to user'), user=u.username, label=label, session=session_name)
    return render_template('session_user_form.html', title=_l('Assign session to user'), form=form)
