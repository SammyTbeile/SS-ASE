from wtforms import Form, StringField, PasswordField, validators

class RegistrationForm(Form):
    username = StringField('Username')
    name = StringField('Name')
    email = StringField('Email Address')
    dorm_building= StringField('Dorm Building')
    phone = StringField('Cell Number')
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class LoginForm(Form):
    username = StringField('Username')
    password = PasswordField('Password')
