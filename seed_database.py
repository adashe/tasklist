"""Script to seed database."""

import os
import json

import crud
import model
import server

os.system("dropdb tasklist")
os.system('createdb tasklist')

model.connect_to_db(server.app)
model.db.create_all()


## ADD USERS ##

user1 = crud.create_user("Andrea", "TEST")
user2 = crud.create_user("Ivan", "TEST")     
user3 = crud.create_user("Seiya", "TEST")     
user4 = crud.create_user("Somi", "TEST")  

users_in_db = [user1, user2, user3, user4]

model.db.session.add_all(users_in_db)


## ADD CHORES ##

chore1 = crud.create_chore("Feed the Dog", "Give 1.5 cups of food twice per day.")
chore2 = crud.create_chore("Give Medicine to Dog", "Give 1/2 pill every 12 hours. Cover with cream cheese.")
chore3 = crud.create_chore("Bark at Squirrels", "Bark at all squirrels to tell them that they are being watched at all times.")
chore4 = crud.create_chore("Run Fast", "Run as fast as possible for as long as possible.")

chores_in_db = [chore1, chore2, chore3, chore4]

model.db.session.add_all(chores_in_db)


## ADD ASSIGNMENTS ##

assignment1 = crud.create_assignment(1, 1)
assignment2 = crud.create_assignment(2, 2)
assignment3 = crud.create_assignment(3, 3)
assignment4 = crud.create_assignment(3, 4)
assignment5 = crud.create_assignment(4, 3)

assignments_in_db = [assignment1, assignment2, assignment3, assignment4, assignment5]

model.db.session.add_all(assignments_in_db)

model.db.session.commit()
