"""Models for tasklist app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))

    def __repr__(self):
        return f'<User user_id={self.user_id} username={self.username}>'


class Group(db.Model):
    """A group."""

    __tablename__ = "groups"

    group_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    group_name = db.Column(db.String(20), unique=True)
    group_description = db.Column(db.Text)

    def __repr__(self):
        return f'<Group group_id={self.group_id} group_name={self.group_name} group_description={self.group_description}>'
    

class GroupUser(db.Model):
    """Many to many relationship between users and groups."""

    __tablename__ = "user_groups"

    group_id = db.Column(db.Integer, 
                        db.ForeignKey('groups.group_id'),
                        primary_key=True)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'),
                        primary_key=True)

    group = db.relationship("Group", backref="user_groups")
    user = db.relationship("User", backref="user_groups")

    def __repr__(self):
        return f'<GroupUser group_id={self.group_id} group_name={self.group.group_name} user_id={self.user_id} username={self.user.username}>'


class Chore(db.Model):
    """A library of chores."""

    __tablename__ = "chores"

    chore_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    chore_name = db.Column(db.String(20), unique=True)
    chore_description = db.Column(db.Text)

    def __repr__(self):
        return f'<Chore chore_id={self.chore_id} chore_name={self.chore_name} description={self.chore_description}>'


class GroupChore(db.Model):
    """Many to many relationship between groups and chores."""

    __tablename__ = "group_chores"

    group_id = db.Column(db.Integer, 
                        db.ForeignKey('groups.group_id'),
                        primary_key=True)
    chore_id = db.Column(db.Integer, 
                        db.ForeignKey('chores.chore_id'),
                        primary_key=True)

    
    group = db.relationship("Group", backref="group_chores")
    chore = db.relationship("Chore", backref="group_chores")

    def __repr__(self):
        return f'<GroupChores group_id={self.group_id} group_name={self.group.group_name} chore_id={self.chore_id} chore_name={self.chore.chore_name}>'


class Assignment(db.Model):
    """Chores that have been assigned to a user."""

    __tablename__ = "assignments"

    assignment_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    chore_id = db.Column(db.Integer, db.ForeignKey('chores.chore_id'))
    complete = db.Column(db.Boolean)

    user = db.relationship("User", backref="assignments")
    chore = db.relationship("Chore", backref="assignments")

    def __repr__(self):
        return f'<Assignment assignment_id={self.assignment_id} user={self.user.username} chore={self.chore.chore_name} complete={self.complete}>'


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
