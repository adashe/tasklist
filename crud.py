"""CRUD operations."""

from model import db, User, Group, Chore, Assignment connect_to_db


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
    """Return the user if exits"""

    return User.query.filter(User.username == username).first()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)


# TODO: Add crud for chores, groups, and assignments and test code.