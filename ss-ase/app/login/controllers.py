# remaining

#controllers
#html


# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module forms
from app.login.forms import LoginForm, RegistrationForm

# Import module models (i.e. User)
from app.login.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
login_auth = Blueprint('login', __name__, url_prefix='/login')

# Set the route and accepted methods
@login_auth.route('/signin/', methods=['GET', 'POST'])


def signin():

    # If sign in form is submitted
    form = LoginForm(request.form)

    # Verify the sign in form
    if form.validate_on_submit():

        #identify our user by their unique username
        user = User(username=form.username.data)

        #if user and check_password_hash(user.password, form.password.data):
        if user:

            session['Username'] = user.username

            flash('Welcome %s' % user.name)

#where to redirect?
            #return redirect(url_for('auth.home'))
            return redirect("/")

        flash('Wrong email or password', 'error-message')

    return render_template("login/signin.html", form=form)


@login_auth.route('/register/', methods=['GET', 'POST'])


def register():

    # If registration is submitted
    form = RegistrationForm(request.form)

    #form.save()
    #if form.save():

        #identify our user by their unique username
        #user = User(username=form.username.data)

        #if user:

        #return redirect("../signin")

    #if request.method == 'POST' and form.validate():
    if form.validate_on_submit():


        user = User(username= form.username.data, name=form.name.data, email=form.email.data, dorm_building=form.dorm_building.data, phone=form.phone.data, password=form.password.data, confirm=form.confirm.data)
        #user = User(form.username.data, form.email.data, form.password.data)
        #db.add(user)
        user.save()
        flash('Thanks for registering')
        return redirect("login/signin")


    return render_template("login/register.html", form=form)
