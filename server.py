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

    if 'user_id' in session:
        return redirect('/tasklist')

    return render_template("homepage.html")


@app.route("/login", methods=['POST'])
def user_login():
    """Check the password and log in."""

    username = request.form['username']
    password = request.form["password"]

    user = crud.get_user_by_username(username)

    if user:
        if user.password == password:
            session['user_id']= user.user_id
            flash('Logged in!')
            return redirect('/tasklist')
        else:
            flash('Wrong password.')
            
    else:
        flash("Please create an account.")

    return redirect('/')


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
        flash("A user with that username already exists. Please enter a different username.")

    return redirect("/")


@app.route("/users")
def show_users():
    """Shows users."""

    users = crud.get_users()

    return render_template("users.html", users=users)


@app.route("/users/<user_id>")
def show_user_profile(user_id):
    """Shows user profiles."""

    user = crud.get_user_by_id(user_id)
    assignments = crud.get_assignments_by_user_id(user_id)

    return render_template("user_profile.html", user=user, assignments=assignments)


@app.route("/tasklist")
def show_tasklist():
    """Shows tasklist."""

    users = crud.get_users()
    chores = crud.get_chores()
    groups = crud.get_groups()

    return render_template("tasklist.html", users=users, chores=chores, groups=groups)


@app.route("/add-assignment", methods=["POST"])
def add_assignment():
    """Create a new assignment."""

    chore_id = request.form['chore_id']
    user_id = request.form["user_id"]
    
    new_assignment = crud.create_assignment(user_id, chore_id)
    db.session.add(new_assignment)
    db.session.commit()
    flash("You have assigned a new chore!")

    return redirect("/tasklist")


@app.route("/groups")
def show_groups():
    """Shows groups."""

    groups = crud.get_groups()

    return render_template("groups.html", groups=groups)


@app.route("/groups/<group_id>")
def show_group_details(group_id):
    """Shows group details."""

    group = crud.get_group_by_id(group_id)

    group_users = crud.get_users_by_group(group_id)
    group_chores = crud.get_chores_by_group(group_id)

    chores = crud.get_chores()
    groups = crud.get_groups()

    return render_template("group_profile.html", group=group, group_users=group_users, group_chores=group_chores, chores=chores, groups=groups)


@app.route("/add-group-chore", methods=["POST"])
def add_group_chore():
    """Add a new chore to the group chore library."""

    chore_id = request.form['chore_id']
    group_id = request.form['group_id']

    new_group_chore = crud.add_chore_to_group(group_id, chore_id)
    db.session.add(new_group_chore)
    db.session.commit()
    flash("You have added a new chore to the group chore library!")

    return redirect("/groups")


@app.route("/add-chore", methods=["POST"])
def add_chore():
    """Create a new chore."""

    chore_name = request.form['chore_name']
    chore_description = request.form["chore_description"]
    
    new_chore = crud.create_chore(chore_name, chore_description)
    db.session.add(new_chore)
    db.session.commit()
    flash("You have added a new chore!")

    return redirect("/tasklist")

# @app.route("/mark-complete", methods=["POST"])
# def mark_complete():

#     assignment_id = request.form['assignment_id']

#     completed_assignment = crud.mark_assignment_complete(assignment_id)   

#     db.session.add(completed_assignment)
#     db.session.commit()

#     return render_template("user_profile.html")


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
