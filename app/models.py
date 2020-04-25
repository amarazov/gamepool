import random
from datetime import datetime
from time import time

import jwt
from flask import current_app
from flask_login import UserMixin
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login
from app.auth import ACCESS

association_table_session_user = db.Table('association_table_session_user', db.Model.metadata,
                                          db.Column('session_id', db.Integer, db.ForeignKey('session.id')),
                                          db.Column('user', db.Integer, db.ForeignKey('user.id')))

association_table_session_game = db.Table('association_table_session_game', db.Model.metadata,
                                          db.Column('session_id', db.Integer, db.ForeignKey('session.id')),
                                          db.Column('game_id', db.Integer, db.ForeignKey('game.id')))

association_table_attempt_answer = db.Table('association_table_attempt_answer', db.Model.metadata,
                                            db.Column('attempt_id', db.Integer, db.ForeignKey('attempt.id')),
                                            db.Column('answer_id', db.Integer, db.ForeignKey('answer.id')))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    answers = db.relationship('Answer', backref=backref('user', uselist=False), lazy='dynamic')
    sessions = db.relationship("Session",
                               secondary=association_table_session_user,
                               backref=backref("users"))
    access = db.Column(db.Integer, default=ACCESS['guest'], nullable=False)
    label = db.Column(db.String(64), index=True, unique=True, nullable=True)

    def set_label(self, token):
        if token:
            decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            self.label = decoded['label']
            self.access = ACCESS['user']

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    def is_admin(self):
        return self.access == ACCESS['admin']

    def allowed(self, access_level):
        return self.access >= access_level

    @staticmethod
    def verify_reset_password_token(token):
        try:
            user_id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(user_id)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    typ = db.Column(db.String(64))
    db.UniqueConstraint('name', 'typ', name='NameTypUnique')
    args = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    answers = db.relationship('Answer', backref='game', lazy='dynamic')

    def __repr__(self):
        return '<Game {};{}:{}>'.format(self.id, self.name, self.typ)

    @property
    def eval(self):
        if self.typ == '*':
            games = list(Game.query.filter_by(name=self.name).filter(Game.typ.notlike('%*%')))
            return random.choice(games)
        if '*' in self.typ:
            games = list(Game.query.filter_by(name=self.name).filter(Game.typ.notlike('%*%'))
                         .filter(Game.typ.like(self.typ.replace('*', '%'))))
            return random.choice(games)
        return self


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    args = db.Column(db.String(500))
    time = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Answer to {};user {}>'.format(self.game_id, self.user_id)


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    attempts = db.relationship('Attempt', backref=backref('session', uselist=False), lazy='dynamic')
    games = db.relationship("Game",
                            secondary=association_table_session_game,
                            backref="sessions")

    def __repr__(self):
        return '<Session {}>'.format(self.id)


class Attempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))

    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    answers = db.relationship("Answer",
                              secondary=association_table_attempt_answer,
                              backref=backref("attempt", uselist=False))

    def __repr__(self):
        return '<Attempt {}>'.format(self.id)


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
