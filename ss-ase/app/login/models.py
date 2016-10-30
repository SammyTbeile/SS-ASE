
from app import db
#from flask.ext.mongoeninge.wtf

#user object
class User (db.Document):
    #specify forms
    name = db.StringField(required=True, unique=True)
    username = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    phone = db.StingField(required=True, unique=True)
    dorm_building = db.StringField(required=True)
    email = db.StringField(required=True, unique=True)
    # list field - hold users lstings
    def is_authenticated(self):
        users = User.object(username=self.username, password=self.password)
        return len(users) != 0
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.name





    #mongoeninge = interface for monogoDB
