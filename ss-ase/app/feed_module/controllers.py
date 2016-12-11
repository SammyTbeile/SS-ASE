import boto3
from boto.s3.key import Key
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Listing

feed_module = Blueprint('start', __name__, url_prefix='/')

AWS_ACCESS_KEY_ID = 'AKIAJWYMQFFTQNTCOGFQ'
AWS_SECRET_ACCESS_KEY = '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'
BUCKET_NAME = 'rags2riches'

session = boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
s3 = session.resource('s3')
s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

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
    return render_template("feed.html", listings=listings, s3=s3_client)

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
        filename = title + '.jpg'
        user = current_user.username
        email = current_user.email

        if not title or not size or not price or (photo.filename == ""):
            error = 1 #required fields are not filled
        elif not isNumber(price) or not isInRange(price, low, high):
            error = 2 #price is not a number and/or not in range
        elif not isWord(title):
            error = 3 #title is garbage value
        elif Listing.objects(title=title):
            error = 4 #title is not unique
        elif not allowed_file(photo.filename):
            error = 5 #not a .jpg file
        if error:
            return render_template("listing.html", error=error, title=title, low=low, high=high)

        else:
            s3.Bucket(BUCKET_NAME).put_object(Key=filename, Body=photo)
            new_list = Listing(title, size, price, info, filename, user, email)
            new_list.save()
            return render_template("confirm.html", title=title)
    else:
        error = 0
        return render_template("listing.html", error=error)

@feed_module.route("listing/<title>")
@login_required
def listing(title):
    item = Listing.objects(title=title)
    return render_template("see_listing.html", item=item[0], s3=s3_client)

@feed_module.route("delete/<title>", methods=["POST"])
@login_required
def delete(title):
	db_item = Listing.objects.get(title=title)
	s3_key = db_item.filename
	# delete listing from db and s3 bucket
	db_item.delete()
	s3.Object(BUCKET_NAME, s3_key).delete()
	return redirect(url_for('.feed'))

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


