"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb tasklist")
os.system('createdb tasklist')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/users.json') as f:
    user_data = json.loads(f.read())

users_in_db = []
for user in user_data:
    username, password = (
        user["username"],
        user["password"],
    )

    db_user = crud.create_user(username, password)
    users_in_db.append(db_user)   

model.db.session.add_all(users_in_db)
model.db.session.commit()

# TODO: Add chores database and test code.