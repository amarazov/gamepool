import jwt
from flask import current_app
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from app.models import User, Session


class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


class RegistrationForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    token = StringField(_l('Label (optional)'), validators=[])
    submit = SubmitField(_l('Register'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_l('Please use a different username.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_l('Please use a different email address.'))

    def validate_token(self, token):
        print(token.data)
        if token.data is None or token.data == '':
            return
        try:
            decoded = jwt.decode(token.data, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user = User.query.filter_by(label=decoded['label']).first()
            if user is not None:
                raise ValidationError(_l('Label already exists. Please use a different label.'))
        except ValidationError as e:
            raise e
        except Exception:
            raise ValidationError(_l('Invalid label. Leave empty if you haven\'t been provided with one.'))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Request Password Reset'))


class LabelRequestForm(FlaskForm):
    label = StringField(_l('Label'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))


class AssignUserToSessionRequestForm(FlaskForm):
    label = StringField(_l('Label'), validators=[DataRequired()])
    session_name = StringField(_l('Session'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

    def validate_label(self, label):
        user = User.query.filter_by(label=label.data).first()
        if user is None:
            raise ValidationError(_l('No user with this label.'))

    def validate_session_name(self, session_name):
        s = Session.query.filter_by(name=session_name.data).first()
        if s is None:
            raise ValidationError(_l('No user with this label.'))
