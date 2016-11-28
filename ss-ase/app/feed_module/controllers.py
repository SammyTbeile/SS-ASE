from flask import Blueprint, render_template, request, send_from_directory
from flask_login import login_required
from .models import Listing
import os

feed_module = Blueprint('start', __name__, url_prefix='/')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
target = os.path.join(APP_ROOT, "../static")
ALLOWED_EXTENSIONS = set(['jpg', 'JPG'])
PRICE_RANGE = [5, 100]
low = PRICE_RANGE[0]
high = PRICE_RANGE[1]

@feed_module.route("")
def welcome():
	return render_template("index.html")

@feed_module.route("feed")
@login_required
def feed():
	listings = Listing.objects()
	return render_template("feed.html", listings=listings, display=send_image)

@feed_module.route("list", methods=["GET", "POST"])
@login_required
def list():
	if request.method == "POST":
		error = 0
		title = request.form["list_title"]
		size = request.form["list_size"]
		price = request.form["list_price"]
		info = request.form["list_info"]
		photo = request.files['file']
		filename = photo.filename

		image_names = os.listdir(target)

		if not title or not size or not price or (filename == ""):
			error = 1 #required fields are not filled
		elif not isNumber(price) or not isInRange(price, low, high):
			error = 2 #price is not a number and/or not in range
		elif not isWord(title):
			error = 3 #title is garbage value
		elif Listing.objects(title=title):
			error = 4 #title is not unique
		elif not allowed_file(filename):
			error = 5 #not a .jpg file
		elif photo.filename in image_names:
			error = 6 #jpg is not unique
	
		if error:
			return render_template("listing.html", error=error, title=title, low=low, high=high)

		else:
			destination = "/".join([target, filename])
			photo.save(destination)

			new_list = Listing(title, size, price, info, filename)
			new_list.save()
			return render_template("confirm.html", title=title)
	else:
		error = 0
		return render_template("listing.html", error=error)

@feed_module.route("listing/<title>")
@login_required
def listing(title):
	item = Listing.objects(title=title)
	return render_template("see_listing.html", item=item[0])

@feed_module.route("images/<filename>")
def send_image(filename):
	return send_from_directory("images", filename)

def isNumber(price):
	try:
		float(price)
		return True
	except ValueError:
		return False

def isInRange(price, low, high):
	price = float(price)
	if (price >= low and price <= high):
		return True
	return False

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def isWord(title):
	if (any(x.isalpha() for x in title) and all(x.isalpha() or x.isspace() for x in title)):
		return True
	return False
