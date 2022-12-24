from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import Email, DataRequired, Length, Regexp

class MyForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(),
                                           Length(
                                               min=4, max=10, message='Name length must be between %(min)d and %(max)d'),
                                           Regexp(regex='^[A-Za-z][A-Za-z0-9_.]*$',
                                                  message='Username can contains lettes, numbers, dots and underscores')])
    email = StringField("Email", validators=[
                        DataRequired(), Email(message='Email is invalid')])
    phone = StringField("Phone", validators=[Regexp(
        regex='^\+380[0-9]{9}$', message='Phone is invalid')])
    subject = SelectField("Subject",
                          choices=[('1', 'Bug report'), ('2', 'Cooperation'), ('3', 'Suggestions')])
    message = TextAreaField("Message", validators=[
                            Length(max=500, message='Message is too long')])
    submit = SubmitField("Send")
