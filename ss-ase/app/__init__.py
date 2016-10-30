from flask import Flask, render_template
from flask_mongoengine import MongoEngine
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

db = MongoEngine(app)

login_manager = LoginManager()
login_manager.init_app(app)


from app.feed_module.controllers import feed_module as start_module
app.register_blueprint(start_module)

from app.login.controllers import login_auth as auth_login

app.register_blueprint(auth_login)
