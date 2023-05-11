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
def checkin_user(badge):
    to_checkin = database_init.session.execute(select(class_models.User)
        .where(class_models.User.badge == badge)).scalar_one_or_none()
    if to_checkin == None:
        print("User is not in the database")
        return
    print("Welcome", to_checkin)
    
# Manager Commands

# Addes a new user, if the ID is not currently present    
def add_new_user(idnumber, access, firstname, lastname, email, role):
    # Check if user already exists
    to_check = database_init.session.execute(select(class_models.User)
        .where(class_models.User.id == idnumber)).scalar_one_or_none()
    # Return if they do
    if to_check != None:
        print("User", to_check, "- ID (", to_check.id, ") is already in the database")
        return
    # Otherwise, add the user to the database
    user = class_models.User(idnumber, access, firstname, lastname, email, role)
    database_init.session.add(user)
    database_init.session.commit()

# Removes a user from the database, if they are present
def remove_user(idnumber):
    # Looks for the User with a matching ID
    to_delete = database_init.session.execute(select(class_models.User)
        .where(class_models.User.id == idnumber)).scalar_one_or_none()
    # If not found, return
    if to_delete == None:
        print("User is not in the database")
        return
    # Else, remove from the database
    database_init.session.delete(to_delete)
    database_init.session.commit()

# Add trainings to a passed User
def add_training(user_id, machine_id):
    # Check to see if the user is in the database
    to_train = database_init.session.execute(select(class_models.User)
        .where(class_models.User.id == user_id)).scalar_one_or_none()
    # If they aren't, leave
    if to_train == None:
        print("User is not in the database")
        return
    # Check to see if the machine is in the database
    machine = database_init.session.execute(select(class_models.Machine)
        .where(class_models.Machine.id == machine_id)).scalar_one_or_none()
    # If is isn't, leave
    if machine == None:
        print("Machine is not in the database")
        return
    to_train.machines.append(machine)
    database_init.session.commit()

# Remove trainings to a passed User
def remove_training(user_id, machine_id):
    # Check to see if the user is in the database
    to_train = database_init.session.execute(select(class_models.User)
        .where(class_models.User.id == user_id)).scalar_one_or_none()
    # If they aren't, leave
    if to_train == None:
        print("User is not in the database")
        return
    # Check to see if the machine is in the database
    machine = database_init.session.execute(select(class_models.Machine)
        .where(class_models.Machine.id == machine_id)).scalar_one_or_none()
    # If is isn't, leave
    if machine == None:
        print("Machine is not in the database")
        return
    to_train.machines.remove(machine)
    database_init.session.commit()

# Output all Machines and user trained on them
def read_all_machines():
    # Current as of SQLAlchemy 2.0
    results = database_init.session.scalars(select(class_models.Machine)).all()
    print(results)

# Currently unused
def user_check(firstname, lastname):
    results = select(class_models.User).where(class_models.User.firstname.in_(firstname))
    for class_models.User in database_init.session.scalars(results):
        print(results)

# Output all users in the database
def read_all():
    # Current as of SQLAlchemy 2.0
    results = database_init.session.scalars(select(class_models.User)).all()

    # Legacy 1.4
    #results = database_init.session.query(class_models.User).all()#.join(class_models.Machine.idnumber == class_models.User.idnumber)

    print(results)

# Method to see who is currently in the lab
def read_all_online():
    results = database_init.session.scalars(select(class_models.User)).all()
    print(results)

def change_user_training(idnumber, machine, trained_status):
    result = select(class_models.User).where(class_models.User.id == idnumber) #join(class_models.Machine).where
    user_to_change = database_init.session.scalars(result).one()
    database_init.session.commit()

# Admin Commands

def change_user_access_level(idnumber, new_access_level):
    result = select(class_models.User).where(class_models.User.id == idnumber)
    to_change = database_init.session.scalars(result).one()
    to_change.role = new_access_level
    database_init.session.commit()