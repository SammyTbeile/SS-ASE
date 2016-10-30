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

        if user and check_password_hash(user.password, form.password.data):

            session['Username'] = user.username

            flash('Welcome %s' % user.name)

#where to redirect?
            #return redirect(url_for('auth.home'))
            return

        flash('Wrong email or password', 'error-message')

    return render_template("login/signin.html", form=form)
