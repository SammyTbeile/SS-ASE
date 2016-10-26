from flask.ext.mongoengine.wtf import model_form

class User(db.Document):
    name = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    def is_authenticated(self):
        users = User.object(name=self.name, password=self.password)
        return len(users) != 0
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.name
