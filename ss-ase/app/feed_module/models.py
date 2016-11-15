from app import db

class Listing(db.Document):
	title = db.StringField(required=True, unique=True)
	size = db.StringField(required=True)
	price = db.StringField(required=True)
	info = db.StringField(required=True)
	filename = db.StringField(required=True)
	def get_title(self):
		return self.title
