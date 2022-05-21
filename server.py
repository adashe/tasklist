"""Server for tasklist app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def show_homepage():
    """Shows homepage."""

    return render_template("homepage.html")


@app.route("/users")
def show_users():
    """Shows users."""

    users = crud.get_users()

    return render_template("users.html", users=users)


@app.route("/users/<user_id>")
def show_user_profile(user_id):
    """Shows user profiles."""

    user = crud.get_user_by_id(user_id)

    return render_template("user_profile.html", user=user)


@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    username = request.form['username']
    password = request.form["password"]
    
    if crud.get_user_by_username(username) is None:
        user = crud.create_user(username, password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has successfully been created. You may now log in.")

    else:
        flash("A user with that email already exists. Please enter a different email.")

    return redirect("/")


@app.route("/tasklist")
def show_tasklist():
    """Shows tasklist."""

    users = crud.get_users()

    return render_template("tasklist.html", users=users)

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
