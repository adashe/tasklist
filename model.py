"""Models for tasklist app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename___ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    # group_name = db.Column(db.Integer, db.ForeignKey('groups.group_name'))

    def __repr__(self):
        return f'<User user_id={self.user_id} username={self.username}>'


# class Group(db.Model):
#     """A group of one or more users."""

#     __tablename___ = "groups"

#     group_id = db.Column(db.Integer,
#                         autoincrement=True,
#                         primary_key=True)
#     group_name = db.Column(db.String(20))

#     def __repr__(self):
#         return f'<Group group_id={self.group_id} group_name={self.group_name}>'


# class Chore(db.Model):
#     """A library of chores."""

#     __tablename___ = "chores"

#     chore_id = db.Column(db.Integer,
#                         autoincrement=True,
#                         primary_key=True)
#     chore_name = db.Column(db.String(20), unique=True)
#     chore_description = db.Column(db.Text)

#     def __repr__(self):
#         return f'<Chore chore_id={self.chore_id} description={self.chore_description}>'


# class Assignment(db.Model):
#     """Chores that have been assigned to a user."""

#     __tablename___ = "assignments"

#     assignment_id = db.Column(db.Integer,
#                         autoincrement=True,
#                         primary_key=True)
#     group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'))
#     chore_id = db.Column(db.Integer, db.ForeignKey('chores.chore_id'))
#     complete = db.Column(db.Boolean)
#     date = db.Column(db.Integer)
#     complete = db.Column(db.Boolean)

    # def __repr__(self):
    #     return f'<Assignment assignment_id={self.assignment_id} group_id={self.group_id} chore_id={self.chore_id}>'


def connect_to_db(app, db_uri="postgresql:///tasklist", echo=True):
    """Connect to database."""

    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql:///tasklist"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)