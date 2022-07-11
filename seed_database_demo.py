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
# create_user(username, password)

user1 = crud.create_user("Seema", "TEST")
user2 = crud.create_user("Andrew", "TEST")     
user3 = crud.create_user("Aubrey", "TEST")     
user4 = crud.create_user("Anika", "TEST")  

users_in_db = [user1, user2, user3, user4]

model.db.session.add_all(users_in_db)


## ADD CHORES ##
# create_chore(chore_name, chore_description)

chore1 = crud.create_chore("Grade assessments", "Grade all ungraded assessments.")
chore2 = crud.create_chore("Answer messages", "Answer messages on Discord.")
chore3 = crud.create_chore("Help students", "Set up meetings to help all students.")
chore4 = crud.create_chore("Fix FRODO", "Figure out what went wrong with FRODO.")
chore5 = crud.create_chore("Make cupcakes", "Make cupcakes for all students.")
chore6 = crud.create_chore("Decorate", "Decorate the Zoom with balloons and streamers.")
chore7 = crud.create_chore("Order pizza", "Order cheese and pepperoni pizza.")
chore8 = crud.create_chore("Prepare milkshakes", "Prepare for vanilla and chocolate milkshakes.")

chores_in_db = [chore1, chore2, chore3, chore4, chore5, chore6, chore7, chore8]

model.db.session.add_all(chores_in_db)


## ADD ASSIGNMENTS ##
# create_assignment(user_id, chore_id, group_id, complete=False)

assignment1 = crud.create_assignment(1, 1, 1)
assignment2 = crud.create_assignment(2, 2, 1)
assignment3 = crud.create_assignment(3, 3, 2)
assignment4 = crud.create_assignment(3, 4, 2)
assignment5 = crud.create_assignment(4, 3, 2)
assignment6 = crud.create_assignment(1, 4, 1)
assignment7 = crud.create_assignment(1, 5, 3)
assignment8 = crud.create_assignment(2, 6, 3)
assignment9 = crud.create_assignment(3, 7, 3)
assignment10 = crud.create_assignment(4, 8, 3)

assignments_in_db = [assignment1, assignment2, assignment3, assignment4, assignment5, assignment6, assignment7, assignment8, assignment9, assignment10]

model.db.session.add_all(assignments_in_db)


## ADD GROUPS ##
# create_group(group_name, group_description)

group1 = crud.create_group("Hackbright Staff", "Staff for the Grace Hackbright cohort")
group2 = crud.create_group("Hackbright TAs", "TAs for the Grace Hackbright cohort")
group3 = crud.create_group("Top Secret", "A secret group for a secret party on July 23, 2022")

groups_in_db = [group1, group2, group3]

model.db.session.add_all(groups_in_db)


## ADD USERS TO GROUP ##
group_user1 = crud.add_user_to_group(1, 1)
group_user2 = crud.add_user_to_group(1, 2)
group_user3 = crud.add_user_to_group(2, 3)
group_user4 = crud.add_user_to_group(2, 4)
group_user5 = crud.add_user_to_group(3, 1)
group_user6 = crud.add_user_to_group(3, 2)
group_user7 = crud.add_user_to_group(3, 3)
group_user8 = crud.add_user_to_group(3, 4)

group_users_in_db = [group_user1, group_user2, group_user3, group_user4, group_user5, group_user6, group_user7, group_user8]

model.db.session.add_all(group_users_in_db)


## ADD CHORES TO GROUP ##

group_chore1 = crud.add_chore_to_group(1, 1)
group_chore2 = crud.add_chore_to_group(1, 2)
group_chore3 = crud.add_chore_to_group(2, 3)
group_chore4 = crud.add_chore_to_group(2, 4)
group_chore5 = crud.add_chore_to_group(3, 1)
group_chore6 = crud.add_chore_to_group(3, 2)
group_chore7 = crud.add_chore_to_group(3, 3)
group_chore8 = crud.add_chore_to_group(3, 4)

group_chores_in_db = [group_chore1, group_chore2, group_chore3, group_chore4, group_chore5, group_chore6, group_chore7, group_chore8]

model.db.session.add_all(group_chores_in_db)


## COMMIT ALL INPUTS TO DATABASE ##

model.db.session.commit()
