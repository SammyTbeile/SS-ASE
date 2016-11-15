
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, abort
from flask_login import LoginManager, login_user, logout_user
from werkzeug import check_password_hash, generate_password_hash
from mongoengine import DoesNotExist, NotUniqueError
from app import db, login_manager
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
            #flash("Invalid username or password")
            error = 'Invalid credentials'

    return render_template('login/signin.html', form=form)

@login_auth.route('/register/', methods=['GET', 'POST'])

def register():

    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        try:
            user = User(username= form.username.data, name=form.name.data, email=form.email.data, dorm_building=form.dorm_building.data, phone=form.phone.data, password=form.password.data, confirm=form.confirm.data)
            user.save()
        except NotUniqueError:
            error = 'Invalid registration'
            return render_template("login/register.html", form=form)

        return redirect("login/signin")

    return render_template("login/register.html", form=form)

@login_auth.route("/logout")
def logout():
    logout_user()
    return redirect("login/signin")
