"""CRUD operations."""

from model import db, User, Chore, connect_to_db

# from model import db, User, Group, Chore, Assignment, connect_to_db

## USER FUNCTIONS ##

def create_user(username, password):
    """Create and return a new user."""

    user = User(username=username, password=password)

    return user


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

    chore = Chore(chore_name=chore_name, chore_description=chore_description)

    return chore


def get_chores():
    """Return all chores."""

    return Chore.query.all()


def get_chore_by_id(chore_id):
    """Return chore details."""

    return Chore.query.get(user_id)


def get_chore_by_chore_name(chore_name):
    """Return the chore description."""

    return Chore.query.filter(Chore.chore_name == chore_name).first()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)


# TODO: Add crud for chores, groups, and assignments and test code.
