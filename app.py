from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# Starts the flask app
app = Flask(__name__)

# Set up a key and type for the database file
app.config["SECRETE_KEY"] = "to"
# Checks if the database file exists
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

# Starts the database file in flask
db = SQLAlchemy(app)


class Form(db.Model):
    """Setup a table for the database file"""
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))


@app.route("/", methods=["Get", "POST"])
def index():
    # Checks if the user posted the data and then stores the user data
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        occupation = request.form["occupation"]

    # Renders the html file
    return render_template("index.html")


app.run(debug=True, port=5001)
