import csv
import os
from getpass import getpass

import click

from app import db
from app.auth.routes import ACCESS
from app.models import Game, Session, User

csv.register_dialect('singlequote', quotechar="'", quoting=csv.QUOTE_ALL)


def register(app):
    @app.cli.group()
    def translate():
        """Translation and localization commands."""
        pass

    @translate.command()
    def update():
        """Update all languages."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system('pybabel update -i messages.pot -d app/translations'):
            raise RuntimeError('update command failed')
        os.remove('messages.pot')

    @translate.command()
    def compile():
        """Compile all languages."""
        if os.system('pybabel compile -d app/translations'):
            raise RuntimeError('compile command failed')

    @translate.command()
    @click.argument('lang')
    def init(lang):
        """Initialize a new language."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system(
                'pybabel init -i messages.pot -d app/translations -l ' + lang):
            raise RuntimeError('init command failed')
        os.remove('messages.pot')

    @app.cli.group()
    def appcfg():
        """Configuration and initialization commands."""
        pass

    @appcfg.command()
    @click.argument('filename')
    def games(filename):
        """Initialize the game settings with csv file"""
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile, dialect='singlequote')
            for row in reader:
                print(row['name'], row['typ'], row['args'])
                game = Game.query.filter_by(name=row['name'], typ=row['typ']).first()
                if game is None:
                    if row['args'] != 'DELETE':
                        game = Game(name=row['name'], typ=row['typ'], args=row['args'])
                        db.session.add(game)
                        star = Game(name=row['name'], typ='*', args='{}')
                        db.session.add(star)
                        db.session.commit()
                else:
                    if row['args'] == 'DELETE':
                        db.session.delete(game)
                    else:
                        game.args = row['args']
                        db.session.add(game)
            db.session.commit()

    @appcfg.command()
    @click.argument('filename')
    def sessions(filename):
        """Initialize the sessions with csv file"""
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile, dialect='singlequote')
            for row in reader:
                name, game_name, game_typ = row['name'], row['game_name'], row['game_typ']
                print(row)
                if game_name == 'DELETE':
                    s = Session.query.filter_by(name=name).first()
                    db.session().delete(s)
                else:
                    game = Game.query.filter_by(name=row['game_name'], typ=row['game_typ']).first()
                    if game is None:
                        raise ValueError("Not a valid game {}:{}.".format(row['game_name'], row['game_typ']))
                    s = Session.query.filter_by(name=name).first()
                    if not s:
                        s = Session(name=name)
                        db.session().add(s)
                    s.games.append(game)
            db.session.commit()

    @appcfg.command()
    @click.argument('username')
    def addadmin(username):
        """Add admin user"""
        pswd = getpass('Password:')
        email = input('Email:')
        admin = User(username=username, email=email, access=ACCESS['admin'])
        admin.set_password(pswd)
        db.session.add(admin)
        db.session().commit()
