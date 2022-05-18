"""CRUD operations."""

from model import db, User, Chore, Assignment, connect_to_db


    ## USER FUNCTIONS ##

def create_user(username, password):
    """Create and return a new user."""

    return User(username=username, password=password)


def get_users():
    """Return all users."""

    return User.query.all()


def get_user_by_id(user_id):
    """Return user details."""

    return User.query.get(user_id)


def get_user_by_username(username):
    """Return the user if exits."""

    return User.query.filter(User.username == username).first()


    ## CHORE FUNCTIONS ##

def create_chore(chore_name, chore_description):
    """Create and return a new chore."""

    return Chore(chore_name=chore_name, chore_description=chore_description)


def get_chores():
    """Return all chores."""

    return Chore.query.all()


def get_chore_by_chore_id(chore_id):
    """Return chore details."""

    return Chore.query.get(chore_id)


def get_chore_descr_by_chore_name(chore_name):
    """Return the chore description."""

    return Chore.query.filter(Chore.chore_name == chore_name).first()


    ## ASSIGNMENT FUNCTIONS ##

def create_assignment(user_id, chore_id, complete=False):
    """Create and return a new assignment."""

    return Assignment(user_id=user_id, chore_id=chore_id, complete=complete)


def get_assignments():
    """Return all assignments."""

    return Assignment.query.all()


def get_assignment_by_assignment_id(assignment_id):
    """Return assignment."""

    return Assignment.query.get(assignment_id)


def get_user_by_assignment_id(assignment_id):
    """Return user."""

    assignment = get_assignment_by_assignment_id(assignment_id)

    return assignment.user


def get_chore_by_assignment_id(assignment_id):
    """Return chore."""

    assignment = get_assignment_by_assignment_id(assignment_id)

    return assignment.chore


def get_assignments_by_user_id(user_id):
    """Return all chores assigned to a user."""

    return Assignment.query.filter(Assignment.user_id == user_id).all()


def mark_assignment_complete(assignment_id):
    """Mark an assignment complete."""

    assignment = get_assignment_by_assignment_id(assignment_id)

    assignment.complete = True
    
    return assignment


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
