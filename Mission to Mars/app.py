from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

#Importing Scrape Mars
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def index():
    listings = mongo.db.listings.find_one()
    return render_template("index.html", mars=listings)


@app.route("/scrape")
def scraper():
    listings = mongo.db.listings
    mars_data = scrape_mars.scrape()
    listings.update({}, mars_data, upsert=True)
    #redirect back to the home page
    #https://develop.mozilla.org/en-US/docs/Web/HTTP/Status/302
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)

