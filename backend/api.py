from datetime import timedelta
from flask import Blueprint, Flask, jsonify, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy

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
    description = db.Column(db.String(500))
    image = db.Column(db.String(100))

    def __init__(self, title, company, description, image):
        self.title = title
        self.company = company
        self.description = description
        self.image = image


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

    def __init__(self, firstName, lastName, descriptemailion, password):
        self.title = title
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password


# we store our permanent session data for 30 minutes
app.permanent_session_lifetime = timedelta(minutes=30)

@app.route("/")
def default():
    return redirect(url_for("pathways"))


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

# This generates all of the 'Pathway' objects in our database
@app.route('/api/pathways/<int:id>', methods=['GET'])
def pathway(id=id):
    pathways_list = Pathway.query.filter_by(id=id)
    pathways = []

    for pathway in pathways_list:
        pathways.append({'title': pathway.title,
                         'company': pathway.company,
                         'description': pathway.description,
                         'image': pathway.image})
    return jsonify({'pathways': pathways})


@app.route('/api/delete_pathway/<id>', methods=['GET','POST'])
def delete_pathway(id=id):
    found_pathway = Pathway.query.filter_by(id=2)
    found_pathway.delete()
    db.session.commit()
    return 'Deleted', 201


@app.route("/api/login", methods=["GET", "POST"])
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

@app.route("/api/signup", methods = ['GET','POST'])
def signup():
    if request.method == "POST":

        user_info = request.get_json()

        new_user = User(firstName=user_info['firstName'],
                            lastName=user_info['lastName'],
                            email=user_info['email'],
                            password=user_info['password'])
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("pathways"))
    else:
        return jsonify({'page' : 'Sign Up'})



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
