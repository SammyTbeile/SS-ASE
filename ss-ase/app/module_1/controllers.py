from flask import render_template, Blueprint
from app.module_1.models import Listing


module_1 = Blueprint('feed', __name__, url_prefix='/feed')


@module_1.route("/feed")
def feed():
	listings = Listing.objects()
	return render_template("feed.html", listings=listings)

@module_1.route("/list")
def list():
	return render_template("listing.html")
