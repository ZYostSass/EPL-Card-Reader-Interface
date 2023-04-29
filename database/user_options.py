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
from sqlalchemy import select

# Universal Commands

# Takes parsed card data and inputs it into the database
# @app.route('/checkin_user/<idnumber>')
def checkin_user(idnumber):
    to_checkin = database_init.session.execute(select(class_models.User).filter_by(id = idnumber)).scalar_one()
    print("Hello")
    
# Manager Commands
    
def add_new_user(idnumber, firstname, lastname, email, role):
    # Check if user already exists
    # Return if they do
    to_check = database_init.session.execute(select(class_models.User).filter_by(id = idnumber)).scalar_one()
    if to_check.id == idnumber:
        print("User", to_check, "ID: (", to_check.id, ") is already in the database")
        return
    # Otherwise, add the user to the database
    user = class_models.User(idnumber, firstname, lastname, email, role)
    #user_training = class_models
    database_init.session.add(user)
    database_init.session.commit()

def remove_user(idnumber):
    database_init.session.delete(idnumber)
    database_init.session.commit()

def user_check(firstname, lastname):
    results = select(class_models.User).where(class_models.User.firstname.in_(firstname))
    for class_models.User in database_init.session.scalars(results):
        print(results)

def read_all():
    # Current as of SQLAlchemy 2.0
    results = database_init.session.scalars(select(class_models.User)).all()

    # Legacy 1.4
    #results = database_init.session.query(class_models.User).all()#.join(class_models.Machine.idnumber == class_models.User.idnumber)

    print(results)

# Function to see who is currently in the lab
def read_all_online():
    results = database_init.session.scalars(select(class_models.User)).all()
    print(results)

def change_user_training(idnumber, machine, trained_status):
    result = select(class_models.User).where(class_models.User.idnumber == idnumber) #join(class_models.Machine).where
    user_to_change = database_init.session.scalars(result).one()
    #user_to_change.firstname = "hi"
    database_init.session.commit()

# Admin Commands

def change_user_access_level(idnumber, new_access_level):
    result = select(class_models.User).where(class_models.User.idnumber == idnumber)
    to_change = database_init.session.scalars(result).one()
    to_change.role = new_access_level
    database_init.session.commit()