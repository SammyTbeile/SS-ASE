from flask import Blueprint, render_template, request
from flask_login import login_required
from .models import Listing

feed_module = Blueprint('start', __name__, url_prefix='/')

@feed_module.route("")
def welcome():
	return render_template("index.html")

@feed_module.route("feed")
@login_required
def feed():
	listings = Listing.objects()
	return render_template("feed.html", listings=listings)

@feed_module.route("list", methods=["GET", "POST"])
@login_required
def list():
	if request.method == "POST":
		new_list = Listing(title=request.form["list_title"], size=request.form["list_size"], price=request.form["list_price"], condition=request.form["list_condition"]);
		new_list.save()
		return render_template("confirm.html", title=request.form["list_title"])
	else:
		return render_template("listing.html")

@feed_module.route("listing/<title>")
@login_required
def listing(title):
	item = Listing.objects(title=title)
	return render_template("see_listing.html", title=title, size=item[0].size, price=item[0].price, condition=item[0].condition)
