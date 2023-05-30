# Students can only log in and out using their ID card via the scanner
# Managers can:
	# Do everything a Student can
	# Add new Students to the tables
	# Change a Student's training on a given machine
	# NOT required to be trained on all machines
# Admins can:
	# Do everything a Manager can do
	# Change a user's access level

from typing import Optional
from bcrypt import checkpw
from . import database_init
from . import class_models
from sqlalchemy import select, func
from datetime import datetime

# Helper Methods

# Checks to see if a given user is in the database, via badge number
# Returns result (either the user or None)
def is_user_badge_present(badge):
    return database_init.session.execute(select(class_models.User)
        .where(class_models.User.badge == badge)).scalar_one_or_none()

# Checks to see if a given user is in the database, via PSU ID
# Returns result (either the user or None)
def is_user_id_present(psu_id):
    return database_init.session.execute(select(class_models.User)
        .where(class_models.User.psu_id == psu_id)).scalar_one_or_none()

# Checks to see if a given machine is in the database, via name
# Returns result (either the user or None)
def is_machine_present(name):
    return database_init.session.execute(select(class_models.Machine)
        .where(class_models.Machine.name == name)).scalar_one_or_none()

# Universal Commands

# Takes parsed card data and inputs it into the database
# Returns either None or the User
# Can be used to access User members
def checkin_user(badge):
    # Checks to see if the user is in the database
    user = is_user_badge_present(badge)
    # If not, leave
    if user == None:
        raise LookupError(f"User with access number {badge} does not exist")
        return None
    
    # If they are, check them in
    # TODO: Add checkouts to the log somewhere
    log = class_models.EventLog.check_in(user)
    database_init.session.add(log)
    database_init.session.commit()
    
    # Return the User checked in
    return user

def access_logs():
    # TODO: add time range filters
    return database_init.session.execute(select(class_models.EventLog)).scalars().all()

# Gets the first name, last name, and id number of a given badge number
# Returns either None or the entire User
def get_user(badge):
    to_display = is_user_badge_present(badge)
    if to_display == None:
        return None
    else:
        return to_display

def get_user_by_psu_id(id): 
    user = database_init.session.execute(select(class_models.User)
        .where(class_models.User.psu_id == id)).scalar_one_or_none()
    if user == None:
        raise ValueError(f"User with PSU ID {id} is not in the database")
    return user


def get_user_by_id(id): 
    user = database_init.session.execute(select(class_models.User)
        .where(class_models.User.id == id)).scalar_one_or_none()
    if user == None:
        raise ValueError(f"User with PSU ID {id} is not in the database")
    return user



def check_user_password(email, password):
    if email is None or password is None:
        return None
    
    user = database_init.session.execute(select(class_models.User)
        .where(class_models.User.email == email)).scalar_one_or_none()

    if user == None:
        raise LookupError(f"User with email {email} does not exist")
    elif user.pw_hash is None:
        raise LookupError(f"User with email {email} is not a manager or admin and so cannot login")
    elif not checkpw(str.encode(password), user.pw_hash):
        raise ValueError(f"Incorrect password for {email}")
    else:
        return user

# Manager Commands

# Addes a new user, if the ID is not currently present    
def add_new_user(psu_id, access, firstname, lastname, email, role):
    # Check if user already exists
    to_check = is_user_id_present(psu_id)
    # Return if they do
    if to_check != None:
        raise ValueError(f"User with ID {psu_id} is already in the database")
    # Otherwise, add the user to the database
    user = class_models.User(psu_id, access, firstname, lastname, email, role)
    database_init.session.add(user)
    database_init.session.commit()

# Removes a user from the database, if they are present
def remove_user(badge_number):
    # Looks for the User with a matching ID
    to_delete = is_user_badge_present(badge_number)
    # If not found, return
    if to_delete is None:
        raise ValueError(f"User with badge {badge_number} does not exist")
    # Else, remove from the database
    else:
        database_init.session.delete(to_delete)
        database_init.session.commit()

# Add new machines to the database
def add_machine (name):
    # Check to see if the machine is already in the database
    machine = is_machine_present(name)
    # If it is, leave
    if machine != None:
        raise ValueError(f"{name} is already in the database")
    # Otherwise, add it to the end of the database
    max_id = database_init.session.query(func.max(class_models.Machine.id)).scalar()
    next_id = (max_id or 0) + 1

    to_add = class_models.Machine(next_id, name)
    database_init.session.add(to_add)
    database_init.session.commit()

# Edit a given machine's name
def edit_machine(name, new_name):
    # Check to see if the machine is already in the database
    machine = is_machine_present(name)
    # If it isn't, leave
    if machine == None:
        raise LookupError(f"Machine with name {name} does not exist")
    # Otherwise, edit it
    machine.name = new_name
    database_init.session.commit()

# Remove a machine from the database
def remove_machine(name):
    # Check to see if the machine is already in the database
    machine = is_machine_present(name)
    # If it is, leave
    if machine == None:
        raise LookupError(f"Machine with name {name} does not exist")
    database_init.session.delete(machine)
    database_init.session.commit()

# Add trainings to a passed User
def add_training(user_badge, machine_id):
    # Check to see if the user is in the database
    to_train = is_user_badge_present(user_badge)
    # If they aren't, leave
    if to_train == None:
        raise LookupError(f"User with Badge {user_badge} does not exist")
    # Check to see if the machine is in the database
    machine = database_init.session.execute(select(class_models.Machine)
        .where(class_models.Machine.id == machine_id)).scalar_one_or_none()
    # If is isn't, leave
    if machine == None:
        raise LookupError(f"Machine with ID {machine_id} does not exist")
    to_train.machines.append(machine)
    database_init.session.commit()

# Remove trainings to a passed User
def remove_training(user_badge, machine_id):
    # Check to see if the user is in the database
    to_untrain = is_user_badge_present(user_badge)
    # If they aren't, leave
    if to_untrain == None:
        raise LookupError(f"User with Badge {user_badge} does not exist")
    # Check to see if the machine is in the database
    # Works off of machine ID rather than name
    machine = database_init.session.execute(select(class_models.Machine)
        .where(class_models.Machine.id == machine_id)).scalar_one_or_none()
    # If is isn't, leave
    if machine == None:
        raise LookupError(f"Machine with ID {machine_id} does not exist")
    # Remove training from the found user
    to_untrain.machines.remove(machine)
    database_init.session.commit()

# Output all Machines, can access trained list
def read_all_machines():
    # Current as of SQLAlchemy 2.0
    results = database_init.session.scalars(select(class_models.Machine)).all()
    return results

# Output all users in the database
def read_all():
    # Current as of SQLAlchemy 2.0
    results = database_init.session.scalars(select(class_models.User)).all()
    return results

# Edit User badge
def edit_user_badge(idnumber, new_badge):
    # Ensure the user is in the database, via ID
    to_edit = is_user_id_present(idnumber)
    # If not, raise an error
    if to_edit is None:
        raise ValueError(f"User with PSU ID {idnumber} does not exist")
    # Otherwise, edit the User's badge
    to_edit.badge = new_badge
    database_init.session.commit()

# Edit User name
def edit_user_name(idnumber, new_first, new_last):
    # Ensure the user is in the database, via ID
    to_edit = is_user_id_present(idnumber)
    # If not, raise an error
    if to_edit is None:
        raise ValueError(f"User with PSU ID {idnumber} does not exist")
    # Otherwise, edit the User's name
    to_edit.firstname = new_first
    to_edit.lastname = new_last
    database_init.session.commit()

# Edit User email
def edit_user_email(idnumber, new_email):
    # Ensure the user is in the database, via ID
    to_edit = is_user_id_present(idnumber)
    # If not, raise an error
    if to_edit is None:
        raise ValueError(f"User with PSU ID {idnumber} does not exist")
    # Otherwise, edit the User's email
    to_edit.email = new_email
    database_init.session.commit()

# # Update user's role for promotion
# def promote_user(idnumber,role):
#     # Check if user already exists
#     to_promote = database_init.session.execute(select(class_models.User)
#         .where(class_models.User.id == idnumber)).scalar_one_or_none()
#     #If not, raise an exception
#     if to_promote == None:
#         raise ValueError(f"User with ID {idnumber} is not in the database")
#     else:   
#         to_promote.role = role
#         database_init.session.update(to_promote)
#         database_init.session.commit()


# Method to see who is currently in the lab
def read_all_online():
    results = database_init.session.scalars(select(class_models.User)).all()
    return results

# Admin Commands

def change_user_access_level(idnumber, new_access_level, password):
    user = is_user_id_present(idnumber)
    if user == None:
        raise LookupError(f"User with ID {idnumber} does not exist")
    if password is None and user.pw_hash is None:
        raise ValueError("User does not have a password, please provide one")
    user.promote(new_access_level, password)
    database_init.session.commit()

# Purge the database of all Users and Machines
def purge_database():
    # I hope you're happy
    class_models.Base.metadata.drop_all()