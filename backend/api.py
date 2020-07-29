from datetime import timedelta

from flask import Blueprint, Flask, jsonify, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy

from forms import LoginForm, PostForm, SignUpForm, email_validator

# Creates the app object that runs our application
app = Flask(__name__)
app.secret_key = "pathways"
# Stops annoying updates from happening 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# This tells Flask that we want to use a sqlite3 database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

# Create the database object that serves our sqlite3 database
db = SQLAlchemy(app)

# This creates a 'Pathway' obj that we can save in our database
class Pathway(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    company = db.Column(db.String(50))
    description = db.Column(db.String(50))
    image = db.Column(db.String(100))

'''
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    company = db.Column(db.String(50))
    description = db.Column(db.String(50))
    image = db.Column(db.String(100))
'''

# we store our permanent session data for 30 minutes
app.permanent_session_lifetime = timedelta(minutes=30)

@app.route("/")
def default():
    return redirect(url_for("home"))


@app.route("/api/")
def home():
    return render_template("home.html")

# This method triggers whenever someone creates a new 'Pathway' object
@app.route("/api/add_pathway", methods=['POST'])
def add_pathway():
    pathway_data = request.get_json()

    new_pathway = Pathway(title=pathway_data['title'],
                          company=pathway_data['company'],
                          description=pathway_data['description'],
                          image=pathway_data['image'])
    db.session.add(new_pathway)
    db.session.commit()
    return 'Added', 201

# This generates all of the 'Pathway' objects in our database
@app.route('/api/pathways')
def pathways():
    pathways_list = Pathway.query.all()
    pathways = []

    for pathway in pathways_list:
        pathways.append({'title': pathway.title,
                         'company': pathway.company,
                         'description': pathway.description,
                         'image': pathway.image})
    return jsonify({'pathways': pathways})


@app.route('/api/delete_pathway')
def delete_pathway():
    found_pathway = Pathway.query.filter_by(title=title).delete()
    for pathway in found_pathway:
        pathway.delete()
        db.session.commit()

@app.route("/api/login", methods=["POST", "GET"])
def login():
    # we are submitting the user information when it is POST
    if request.method == "POST":
        session.permanent = True
        # this gives us the data inputted by login.html form
        user = request.form["nm"]
        session["user"] = user
        return redirect(url_for("user"))
    # we are just loading the page when it is GET
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/api/signup")
def signup():
    return render_template("signup.html")


@app.route("/api/user")
def user():
    if "user" in session:
        # retrieve the user's name from the dictionary and display it
        user = session["user"]
        return f"<h1>{user}</h1>"
    else:
        return redirect(url_for("login"))


@app.route("/api/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
