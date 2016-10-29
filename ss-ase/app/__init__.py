from flask import Flask, render_template
from flask_mongoengine import MongoEngine
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

db = MongoEngine(app)

login_manager = LoginManager()
login_manager.init_app(app)

from app.module_1.controllers import module_1 as start_module
app.register_blueprint(start_module)
