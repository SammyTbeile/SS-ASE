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

class Listing(db.Document):
	title = db.StringField(required=True, unique=True)
	size = db.StringField(required=True)
	price = db.StringField(required=True)
	condition = db.StringField(required=True)
	def get_title(self):
		return self.title
	def get_size(self):
		return self.size
	def get_price(self):
		return self.price
	def get_condition:
		return self.condition
