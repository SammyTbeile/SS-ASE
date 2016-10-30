from flask import Flask, render_template
from flask_mongoengine import MongoEngine
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

db = MongoEngine(app)

login_manager = LoginManager()
login_manager.init_app(app)


# Import a module / component using its blueprint handler variable (mod_auth)
from app.login.controllers import login_auth as auth_login

# Register blueprint(s)
app.register_blueprint(auth_login)
