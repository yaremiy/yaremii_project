from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from flask_wtf.file import FileField, FileAllowed
from werkzeug.security import check_password_hash

from .models import User

class RegistrationForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(),
                                       Length(
                                           min=4, max=14, message='Name length must be between %(min)d and %(max)d'),
                                       Regexp(regex='^[A-Za-z][A-Za-z0-9_.]*$',
                                              message='Username can contains lettes, numbers, dots and underscores')])
    email = StringField("Email", validators=[
                        DataRequired(), Email(message='Email is invalid')])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6,
                                                                message='Password must be longer than 6 symbols')])
    confirm_password = PasswordField('Confirm password',
                                     validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign up")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[
                        DataRequired(), Email(message='Email is invalid')])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(),
                                       Length(min=4, max=25,
                                              message='Username length must be between 4 and 25'),
                                       Regexp(regex='^[A-Za-z][A-Za-z0-9_.]*$',
                                              message='Username must contain only lettes, numbers, dots and underscores')])
    email = StringField("Email", validators=[DataRequired(), Email()])
    about_me = TextAreaField("About me", validators=[Length(max=120, message='About me is too long')])
    picture = FileField("Profile picture", validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Update")

    def validate_email(self, field):
        if field.data != current_user.email:
            if User.query.filter_by(email=field.data).first():
                raise ValidationError('Email is already registered')

    def validate_username(self, field):
        if field.data != current_user.username:
            if User.query.filter_by(username=field.data).first():
                raise ValidationError('Username is already taken')


class ResetPasswordForm(FlaskForm):
    old_password = PasswordField('Old password')
    new_password = PasswordField('New password',
                             validators=[Length(min=6,
                                                message='Password must be longer than 6')])
    confirm_password = PasswordField('Confirm password',
                                     validators=[DataRequired(), EqualTo("new_password")])
    submit = SubmitField("Reset password")

    def validate_old_password(self, old_password):
        if not check_password_hash(current_user.password, old_password.data):
            raise ValidationError('Password is not correct')
