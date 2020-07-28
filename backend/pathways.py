from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta


app = Flask(__name__)
app.secret_key = "pathways"
app.permanent_session_lifetime = timedelta(minutes=30) # we store our permanent session data for 10 minutes

# Shows the home page for the website with inline HTML
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"] # this gives us the data inputted by login.html form, because this is a dict
        session["user"] = user
        return redirect(url_for("user"))
    else:    
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")
    
@app.route("/user")
def user():
    if "user" in session:
        user = session["user"] #retrieve the user's name from the dictionary and display it
        return f"<h1>{user}</h1>"
    else:
        return redirect(url_for("login"))

@app.route("/opportunity")
def opportunity():
    return render_template("opportunity.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# What makes the application actually run
if __name__ == "__main__":
    app.run(debug=True)