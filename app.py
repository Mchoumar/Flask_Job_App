from datetime import datetime
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from os import getenv

# Starts the flask app
app = Flask(__name__)

# Set up a key and type for the database file
app.config["SECRET_KEY"] = "to"
# Checks if the database file exists
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

# Set up for email host, port, username, and password
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "test"
app.config["MAIL_PASSWORD"] = getenv("PASSWORD")

# Starts the database file in flask
db = SQLAlchemy(app)

# Uses the data provided in the email setup to send the email
mail = Mail(app)


class Form(db.Model):
    """Set up a table for the database file"""
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
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        occupation = request.form["occupation"]

        # Add the data into the table
        form = Form(first_name=first_name, last_name=last_name, email=email,
                    date=date_obj, occupation=occupation)

        # Inserts the data into the database file
        db.session.add(form)
        db.session.commit()

        message_body = f"Thank you for your submission, {first_name}.\n" \
                       f"Here are your data:\n{first_name}\n{last_name}\n{date}\n" \
                       f"Thank you!"
        # Send message
        message = Message(subject="New form submission",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[email],
                          body=message_body)
        mail.send(message)

        # Tells the user that the form was submitted
        flash(f"{first_name}, your form was submitted successfully!", "success")

    # Renders the html file
    return render_template("index.html")


if __name__ == '__main__':
    # Creates the database
    with app.app_context():
        db.create_all()

    # Starts the debugging process for the flask app
    app.run(debug=True, port=5001)
