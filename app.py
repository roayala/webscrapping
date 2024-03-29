from scrape import scrape_mars
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import SubmitField

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Create an instance of our Flask app.
app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecretkey"

# Create connection variable
# conn = 'mongodb://localhost:27017'
conn = "mongodb+srv://m001-student:m001-mongodb-basics@roas15-30p3e.mongodb.net"

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
mars_db = client.mars_db

# Drops collection if available to remove duplicates
mars_db.mars_data.drop()

# Scrape the web
x = scrape_mars.scrape()

# Creates a collection in the database and inserts two documents
mars_db.mars_data.insert_many(x)


class InfoForm(FlaskForm):
    submit = SubmitField("Scrape")


# Set route
@app.route("/index.html")
@app.route("/", methods=["GET", "POST"])
def index():

    # Store the entire team collection in a list
    mars_list = list(mars_db.mars_data.find())
    print(mars_list)

    form = InfoForm()
    if form.validate_on_submit():
        x = scrape_mars.scrape()
        mars_db.mars_data.insert_many(x)
        return render_template("index.html", form=form, mars=mars_list)
    # Return the template with the teams list passed in
    return render_template("index.html", form=form, mars=mars_list)


if __name__ == "__main__":
    app.run(debug=True)
