from flask_wtf import Form
from wtforms import StringField, PasswordField, validators
from flask_mongoengine.wtf import model_form
from wtforms.validators import Required, EqualTo, DataRequired

class RegistrationForm(Form):
    username = StringField('Username')
    name = StringField('Name')
    email = StringField('Email Address', [validators.Email()])
    dorm_building= StringField('Dorm Building')
    phone = StringField('Cell Number')
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class LoginForm(Form):
    username = StringField('Username', [Required(message='Forgot your username?')])
    password = PasswordField('Password', [Required(message='Must provide a password')])
