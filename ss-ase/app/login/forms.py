from flask_wtf import Form
from wtforms import StringField, PasswordField, validators, IntegerField
from wtforms.validators import Required, EqualTo, DataRequired

class RegistrationForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    name = StringField('Name', [validators.DataRequired()])
    email = StringField('Email Address', [validators.DataRequired(), validators.Email()])
    dorm_building = StringField('Dorm Building', [validators.DataRequired()])
    phone = IntegerField('Cell Number', [validators.DataRequired(),
                                         validators.NumberRange(min=1000000000,
                                                                max=9999999999)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password', [validators.DataRequired()])


class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired(),
                                        Required(message='Forgot your username?')])
    password = PasswordField('Password', [validators.DataRequired(),
                                          Required(message='Must provide a password')])
