
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from flask_login import LoginManager, login_user, logout_user
from werkzeug import check_password_hash, generate_password_hash

from app import db

from app.login.forms import LoginForm, RegistrationForm

from app.login.models import User

login_auth = Blueprint('login', __name__, url_prefix='/login')

@login_auth.route('/signin/', methods=['GET', 'POST'])

def signin():

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        if user.is_authenticated:
            login_user(user)
            session['Username'] = user.username

            return redirect('/')

    return render_template("login/signin.html", form=form)


@login_auth.route('/register/', methods=['GET', 'POST'])

def register():

    form = RegistrationForm(request.form)

    if form.validate_on_submit():

        user = User(username= form.username.data, name=form.name.data, email=form.email.data, dorm_building=form.dorm_building.data, phone=form.phone.data, password=form.password.data, confirm=form.confirm.data)

        user.save()

        return redirect("login/signin")

    return render_template("login/register.html", form=form)
