"""Server for tasklist app."""

from flask import Flask, render_template, request, flash, session, redirect, url_for
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

from datetime import datetime, date  ## Google Cal API
from time import strftime, strptime             ## Google Cal API
import os                                       ## Google Cal API
import google.oauth2.credentials                ## Google Cal API
import google_auth_oauthlib.flow                ## Google Cal API
import googleapiclient.discovery                ## Google Cal API

CLIENT_SECRETS_FILE = "client_secret.json"              ## Google Cal API
SCOPES = ['https://www.googleapis.com/auth/calendar']   ## Google Cal API

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' ## Sidesteps need for https
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'  ## Sidesteps need for https

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
            session['user_id'] = user.user_id
            flash('Logged in!')
            return redirect('/tasklist')
        else:
            flash('Wrong password.')
            
    else:
        flash("Please create an account.")

    return redirect('/')


@app.route("/logout")
def user_logout():
    """Log out."""

    if 'user_id' in session:
        del session['user_id']
        flash("You have been logged out.")

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

    if 'user_id' not in session:
        return redirect('/')

    users = crud.get_users()

    return render_template("users.html", users=users)


@app.route("/users/<user_id>")
def show_user_profile(user_id):
    """Shows user profiles."""

    if 'user_id' not in session:
        return redirect('/')

    user = crud.get_user_by_id(user_id)
    assignments = crud.get_assignments_by_user_id(user_id)

    return render_template("user_profile.html", user=user, assignments=assignments)


@app.route("/tasklist")
def show_tasklist():
    """Shows tasklist."""

    if 'user_id' not in session:
        return redirect('/')

    user_id = session['user_id']

    users = crud.get_users()
    chores = crud.get_chores()
    users_groups = crud.get_groups_by_user_id(user_id) #only show groups for this user
    groups = crud.get_groups()

    return render_template("tasklist.html", users=users, chores=chores, users_groups=users_groups, groups=groups)


@app.route("/add-assignment", methods=["POST"])
def add_assignment():
    """Create a new assignment."""

    chore_id = request.form["chore_id"]
    user_id = request.form["user_id"]
    group_id = request.form["group_id"]
    
    new_assignment = crud.create_assignment(user_id, chore_id, group_id)
    db.session.add(new_assignment)
    db.session.commit()

    flash("You have assigned a new task!")

    return redirect(f'/groups/{ group_id }')


@app.route("/groups")
def show_groups():
    """Shows groups."""

    if 'user_id' not in session:
        return redirect('/')

    groups = crud.get_groups()

    return render_template("groups.html", groups=groups)


@app.route("/add-group", methods=["POST"])
def add_group():
    """Create a new group and add user to that group."""

    # Create a new group

    group_name = request.form['group_name']
    group_description = request.form["group_description"]
    
    new_group = crud.create_group(group_name, group_description)
    db.session.add(new_group)

    db.session.commit()

    # Add the user to the new group

    user_id = session['user_id']
    group_id = new_group.group_id

    new_group_user = crud.add_user_to_group(group_id, user_id)
    db.session.add(new_group_user)

    db.session.commit()

    flash("You have created and joined a new group!")

    return redirect("/tasklist")


@app.route("/groups/<group_id>")
def show_group_details(group_id):
    """Shows group details."""

    if 'user_id' not in session:
        return redirect('/')

    group = crud.get_group_by_id(group_id)

    group_users = crud.get_users_by_group(group_id)
    group_chores = crud.get_chores_by_group(group_id)

    chores = crud.get_chores()
    groups = crud.get_groups()
    users = crud.get_users()

    group_user_assignments = crud.group_user_assignments(group_id)

    return render_template(
        "group_profile.html", 
        group_id=group_id, 
        group=group, 
        group_users=group_users, 
        group_chores=group_chores, 
        chores=chores, 
        groups=groups, 
        users=users,
        group_user_assignments=group_user_assignments
        )


@app.route("/add-group-chore", methods=["POST"])
def add_group_chore():
    """Add a new chore to the group chore library."""

    chore_id = request.form['chore_id']
    group_id = request.form['group_id']

    new_group_chore = crud.add_chore_to_group(group_id, chore_id)
    db.session.add(new_group_chore)
    db.session.commit()

    flash("You have added a new task to the group library!")

    return redirect(f'/groups/{ group_id }')


@app.route("/add-chore", methods=["POST"])
def add_chore():
    """Create a new chore."""

    chore_name = request.form['chore_name']
    chore_description = request.form["chore_description"]
    group_id = request.form['group_id']
    
    new_chore = crud.create_chore(chore_name, chore_description)
    db.session.add(new_chore)
    db.session.commit()

    flash("You have added a new task!")

    ## Add chore to the library 

    chore_id = new_chore.chore_id

    new_group_chore = crud.add_chore_to_group(group_id, chore_id)
    db.session.add(new_group_chore)
    db.session.commit()

    flash("You have added a new task to the group library!")

    return redirect(f'/groups/{ group_id }')


@app.route("/add-group-user", methods=["POST"])
def add_group_user():
    """Add a new user to the group."""

    user_id = request.form['user_id']
    group_id = request.form['group_id']

    new_group_user = crud.add_user_to_group(group_id, user_id)
    db.session.add(new_group_user)
    db.session.commit()

    flash("You have added a new user to the group!")

    return redirect(f'/groups/{ group_id }')


@app.route("/join-group", methods=["POST"])
def join_group():
    """Add user to a group."""

    user_id = session['user_id']
    group_id = request.form['group_id']

    new_group_user = crud.add_user_to_group(group_id, user_id)
    db.session.add(new_group_user)
    db.session.commit()

    flash("You have joined a group!")

    return redirect(f'/tasklist')

@app.route("/toggle-complete", methods=["POST"])
def mark_complete():

    assignment_id = request.form['assignment_id']
    user_id = request.form['user_id']
    group_id = request.form['group_id']

    crud.toggle_complete(assignment_id)   

    db.session.commit()

    flash("You have changed the task status!")

    return redirect(f'/groups/{ group_id }')


@app.route("/toggle-complete-from-profile", methods=["POST"])
def mark_complete_from_profile():

    assignment_id = request.form['assignment_id']
    user_id = request.form['user_id']

    crud.toggle_complete(assignment_id)   

    db.session.commit()

    flash("You have changed the task status!")

    return redirect(f'/users/{ user_id }')


@app.route("/delete-assignment", methods=["POST"])
def delete_assignment():

    assignment_id = request.form['assignment_id']
    user_id = request.form['user_id']
    group_id = request.form['group_id']

    assignment = crud.get_assignment_by_assignment_id(assignment_id)

    db.session.delete(assignment)
    db.session.commit()

    flash("You have deleted an assigned task!")

    return redirect(f'/groups/{ group_id }')


@app.route("/delete-assignment-from-profile", methods=["POST"])
def delete_assignment_from_profile():

    assignment_id = request.form['assignment_id']
    user_id = request.form['user_id']
    group_id = request.form['group_id']

    assignment = crud.get_assignment_by_assignment_id(assignment_id)

    db.session.delete(assignment)
    db.session.commit()

    flash("You have deleted an assigned task!")

    return redirect(f'/users/{ user_id }')


@app.route("/delete-group-user", methods=["POST"])
def delete_group_user():

    user_id = request.form['user_id']
    group_id = request.form['group_id']

    group_user = crud.get_group_user(group_id, user_id)
    group_user_assignments = crud.get_assignments_by_group_user(group_id, user_id)

    for group_user_assignment in group_user_assignments:
        db.session.delete(group_user_assignment)

    db.session.delete(group_user)

    db.session.commit()

    flash("You have removed a user and their assigned tasks from this group!")

    return redirect(f'/groups/{ group_id }')


@app.route("/delete-group", methods=["POST"])
def delete_group():

    group_id = request.form['group_id']

    group = crud.get_group_by_id(group_id)
    group_users = crud.get_users_by_group(group_id)
    group_chores = crud.get_chores_by_group(group_id)
    group_assignments = crud.get_assignments_by_group_id(group_id)

    for group_user in group_users:
        db.session.delete(group_user)

    for group_chore in group_chores:
        db.session.delete(group_chore)

    for group_assignment in group_assignments:
        db.session.delete(group_assignment)

    db.session.delete(group)

    db.session.commit()

    flash("You have deleted a group and all of its data!")

    return redirect("/")


## Google Cal API Functions

@app.route('/google-cal')
def show_google_cal():
    """Shows google_cal.html"""

    return render_template("google_cal.html")


@app.route('/authorize')
def authorize():
    """Authorizes Google Calendar."""

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret.json', scopes=SCOPES
        )
    flow.redirect_uri = url_for('oauth2callback', _external=True)
    authorization_url, state = flow.authorization_url(
        access_type = 'offline',
        included_grant_scopes = 'true'
    )

    flash("Your Google Calendar has been authorized.")

    return redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    """Sets credentials."""

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES
    )

    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

    print(session['credentials'])

    return redirect('/google-cal')


@app.route('/add-event', methods=["POST"])
def add_event():
    """Add a Google Calendar event."""

    calendar = request.form.get('calendar')     ## Ask why this is necessary?
    if calendar:
        if not session.get('credentials'):
            flash('Please authorize Tasklist with Google Calendar and try again.')
            return redirect('/authorize')

    description = request.form.get('description') 
    user_id = session['user_id']
    starting_date = request.form.get('date')
    time = request.form.get('time')
    # repeat = request.form.get('repeat')

    starting_date = datetime.strptime(starting_date, '%Y-%m-%d')

    if calendar:
        starting_date = starting_date.strftime('%Y-%m-%d')
        credentials = google.oauth2.credentials.Credentials(**session['credentials'])
        service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

        event = {
        'summary': f'{ calendar }',
        # 'location': '800 Howard St., San Francisco, CA 94103',
        'description': f'{ description }',
        'start': {
            'dateTime': f'{ starting_date }T{ time }:00',
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': f'{ starting_date }T{ time }:59',
            'timeZone': 'America/Los_Angeles',
        },
        # 'recurrence': [
        #     'RRULE:FREQ=DAILY;COUNT=2'
        # ],
        # 'attendees': [
        #     {'email': 'lpage@example.com'},
        #     {'email': 'sbrin@example.com'},
        # ],
        # 'reminders': {
        #     'useDefault': False,
        #     'overrides': [
        #     {'method': 'email', 'minutes': 24 * 60},
        #     {'method': 'popup', 'minutes': 10},
        #     ],
        # },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()

        flash("""Event created: %s """ % (event.get('htmlLink')))

        return redirect('/google-cal')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
