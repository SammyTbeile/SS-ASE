
from flask import Blueprint, request, render_template, redirect
from flask_login import login_user, logout_user
from mongoengine import DoesNotExist, NotUniqueError, ValidationError
from app.login.forms import LoginForm, RegistrationForm
from app.login.models import User

login_auth = Blueprint('login', __name__, url_prefix='/login')

@login_auth.route('/signin/', methods=['GET', 'POST'])
def signin():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        try:
            user = User.objects.get(username=form.username.data, password=form.password.data)
            if user.is_authenticated:
                login_user(user)
                user.authenticated = True
                return redirect('/feed')
        except DoesNotExist:
            error = 'Invalid Username or Password'
            return render_template("login/signin.html", form=form, error=error)
        except ValidationError:
            error = 'Invalid Username or Password - does not exist'
            return render_template("login/signin.html", form=form, error=error)

    return render_template('login/signin.html', form=form)

@login_auth.route('/register/', methods=['GET', 'POST'])

def register():

    form = RegistrationForm(request.form)
    if request.method == 'POST':

        if not form.validate_on_submit():
            error = 'Invalid registration: See marked fields below'
            return render_template("login/register.html", form=form, error=error)

        try:
            user = User(username=form.username.data, name=form.name.data,
                        email=form.email.data, dorm_building=form.dorm_building.data,
                        phone=form.phone.data, password=form.password.data,
                        confirm=form.confirm.data)
            user.save()

        except NotUniqueError:
            error = 'Username is not unique: please try another username'
            return render_template("login/register.html", form=form, errorUsername=error)

        return redirect("login/signin")
    return render_template("login/register.html", form=form)

@login_auth.route("/logout")
def logout():
    logout_user()
    return redirect("login/signin")
