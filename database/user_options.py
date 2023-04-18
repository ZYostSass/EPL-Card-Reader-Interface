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
    print("Hello")
    
# Manager Commands
    
def add_new_user(idnumber, accessnumber, role, firstname, lastname):
    # Check if user already exists
    # Return if they do
    #to_check = select(class_models.User).where(class_models.User.idnumber == idnumber)
    to_check = database_init.session.query(class_models.User).where(class_models.User.idnumber == idnumber)
    print(to_check)
    user = class_models.User(idnumber, accessnumber, role, firstname, lastname)
    # TODO - Set trainning values
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
    #results = select(class_models.User).join(class_models.Machine).where(class_models.User.idnumber == class_models.Machine.idnumber)
    #results = database_init.session.query(class_models.User).select_from(class_models.User).join(class_models.Machine).filter(class_models.User.idnumber == class_models.Machine.idnumber)
    
    # Legacy 1.4 - TODO: Update?
    results = database_init.session.query(class_models.User).all()#.join(class_models.Machine.idnumber == class_models.User.idnumber)

    # results.extend(database_init.session.query(class_models.Machine).all())
    print(results)
    #for class_models.User in database_init.session.scalars(results):
        #print(results)

def change_user_training(idnumber, machine, trained_status):
    result = select(class_models.User).where(class_models.User.idnumber == idnumber) #join(class_models.Machine).where
    user_to_change = database_init.session.scalars(result).one()
    #user_to_change.firstname = "hi"
    database_init.session.commit()

# Admin Commands

def chance_user_access_level(idnumber, new_access_level):
    result = select(class_models.User).where(class_models.User.idnumber == idnumber)
    to_change = database_init.session.scalars(result).one()
    to_change.role = new_access_level
    database_init.session.commit()