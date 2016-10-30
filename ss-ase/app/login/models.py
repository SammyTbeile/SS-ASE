
from app import db

class User (db.Document):

    name = db.StringField(required=True, unique=True)
    username = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    phone = db.StringField(required=True, unique=True)
    dorm_building = db.StringField(required=True)
    email = db.StringField(required=True, unique=True)
    confirm = db.StringField(required=True)

    def is_authenticated(self):
        users = User.object(username=self.username, password=self.password)
        return len(users) != 0
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.name
