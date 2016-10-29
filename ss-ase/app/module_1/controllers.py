from flask import Blueprint, render_template, request
from .models import Listing

module_1 = Blueprint('start', __name__, url_prefix='/')

@module_1.route("")
def welcome():
	return render_template("index.html")

@module_1.route("feed")
def feed():
	listings = Listing.objects()
	return render_template("feed.html", listings=listings)

@module_1.route("list", methods=["GET", "POST"])
def list():
	if request.method == "POST":
		new_list = Listing(title=request.form["list_title"], size=request.form["list_size"], price=request.form["list_price"], condition=request.form["list_condition"]);
		new_list.save()
		return render_template("confirm.html", title=request.form["list_title"])
	else:
		return render_template("listing.html")

@module_1.route("listing/<title>")
def listing(title):
	item = Listing.objects(title=title)
	return render_template("see_listing.html", title=title, size=item[0].size, price=item[0].price, condition=item[0].condition)
