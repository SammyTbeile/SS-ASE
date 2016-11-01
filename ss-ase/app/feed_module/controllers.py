from flask import Blueprint, render_template, request
from .models import Listing

feed_module = Blueprint('start', __name__, url_prefix='/')

@feed_module.route("")
def welcome():
	return render_template("index.html")

@feed_module.route("feed")
def feed():
	listings = Listing.objects()
	return render_template("feed.html", listings=listings)

@feed_module.route("list", methods=["GET", "POST"])
def list():
	if request.method == "POST":
		error = 0
		title = request.form["list_title"]
		size = request.form["list_size"]
		price = request.form["list_price"]
		info = request.form["list_info"]
		if not title or not size or not price:
			error = 1 #required fields are not filled
			return render_template("listing.html", error=error)
		elif not isNumber(price):
			error = 2 #price is not a number
			return render_template("listing.html", error=error)
		elif Listing.objects(title=title):
			error = 3 #title is not unique
			return render_template("listing.html", error=error, title=title)
		else: 
			new_list = Listing(title, size, price, info)
			new_list.save()
			return render_template("confirm.html", title=title)
	else:
		error = 0
		return render_template("listing.html", error=error)

@feed_module.route("listing/<title>")
def listing(title):
	item = Listing.objects(title=title)
	return render_template("see_listing.html", title=title, size=item[0].size, price=item[0].price, info=item[0].info)

def isNumber(price):
	try:
		float(price)
		return True
	except ValueError:
		return False

	
