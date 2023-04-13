# Students can only log in and out using their ID card via the scanner
# Managers can:
	# Do everything a Student can
	# Add new Students to the tables
	# Change a Student's training on a given machine
	# NOT required to be trained on all machines
# Admins can:
	# Do everything a Manager can do
	# Change a user's access level

import database_init
import class_models
# from flask import Flask
# app = Flask(__name__)

# Universal Commands

# Takes parsed card data and inputs it into the database
# @app.route('/checkin_user/<idnumber>')
def checkin_user(idnumber):
    print("Hello")
    
# Manager Commands
    
def add_new_user(idnumber, accessnumber, role, firstname, lastname):
    user = class_models.User(idnumber, accessnumber, role, firstname, lastname)
    database_init.session.add(user)
    # Set trainning values
    # TODO ^
    database_init.session.commit()
    
def user_check(firstname, lastname):
    results = database_init.session.query(class_models.User).all()
    results.extend(database_init.session.query(class_models.Machine).all())
    print(results)
    
def change_user_training(idnumber, machine, trained_status):
    print("Hello")

# Admin Commands

def chance_user_access_level(idnumber):
    print("Hello")