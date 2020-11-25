from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

@app.route("/")
def home():

    mars_data = mongo.db.collection.find_one()
    return render_template("index.html", home=mars_data)


# Route that will trigger the scrape function

@app.route("/scrape")
def scrape():

    #Run scrape function
    mars_data = scrape_mars.scrape_all()

    #Update Mongo DB using update and upsert

    mongo.db.collection.update({}, mars_data, upsert=True)

    #Redirect to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)