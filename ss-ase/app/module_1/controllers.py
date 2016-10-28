from flask import render_template

@app.route("/feed")
def feed():
	listings = Listing.objects()
	return render_template("feed.html", listings=listings)

@app.route("/list")
def list():
	return render_template("listing.html")
