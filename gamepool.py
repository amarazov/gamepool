from app import create_app, cli
from app.models import *

application = create_app()
cli.register(application)


@application.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Game': Game, 'Session': Session, 'Answer': Answer, 'Attempt': Attempt}


if __name__ == '__main__':
    application.run(host='0.0.0.0')
