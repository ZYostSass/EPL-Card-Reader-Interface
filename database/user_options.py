# Students can only log in and out using their ID card via the scanner
# Managers can:
	# Do everything a Student can
	# Add new Students to the tables
	# Change a Student's training on a given machine
	# NOT required to be trained on all machines
# Admins can:
	# Do everything a Manager can do
	# Change a user's access level

from bcrypt import checkpw
from . import database_init
from . import class_models
from sqlalchemy import select, func

# Helper Methods

# Checks to see if a given user is in the database, via badge number
# Returns result (either the user or None)
def is_user_badge_present(badge):
    return database_init.session.execute(select(class_models.User)
        .where(class_models.User.badge == badge)).scalar_one_or_none()

# Checks to see if a given user is in the database, via ID Number
# Returns result (either the user or None)
def is_user_id_present(idnumber):
    return database_init.session.execute(select(class_models.User)
        .where(class_models.User.id == idnumber)).scalar_one_or_none()

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
    to_checkin = is_user_badge_present(badge)
    # If not, leave
    if to_checkin == None:
        raise LookupError(f"User with access number {badge} does not exist")
        return None
    # Return the User checked in
    return to_checkin

# Gets the first name, last name, and id number of a given badge number
# Returns either None or the entire User
def get_user(badge):
    to_display = is_user_badge_present(badge)
    if to_display == None:
        return None
    else:
        return to_display

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
        return None
    elif not checkpw(str.encode(password), user.pw_hash):
        return None
    else:
        return user

# Manager Commands

# Addes a new user, if the ID is not currently present    
def add_new_user(idnumber, access, firstname, lastname, email, role, login):
    # Check if user already exists
    to_check = is_user_id_present(idnumber)
    # Return if they do
    if to_check != None:
        raise ValueError(f"User with ID {idnumber} is already in the database")
    # Otherwise, add the user to the database
    user = class_models.User(idnumber, access, firstname, lastname, email, role, login)
    database_init.session.add(user)
    database_init.session.commit()

# Removes a user from the database, if they are present
def remove_user(idnumber):
    # Looks for the User with a matching ID
    to_delete = is_user_id_present(idnumber)
    # If not found, return
    if to_delete is None:
        raise ValueError(f"User with PSU ID {idnumber} does not exist")
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
def add_training(user_id, machine_id):
    # Check to see if the user is in the database
    to_train = is_user_id_present(user_id)
    # If they aren't, leave
    if to_train == None:
        raise LookupError(f"User with ID {user_id} does not exist")
    # Check to see if the machine is in the database
    machine = database_init.session.execute(select(class_models.Machine)
        .where(class_models.Machine.id == machine_id)).scalar_one_or_none()
    # If is isn't, leave
    if machine == None:
        raise LookupError(f"Machine with ID {machine_id} does not exist")
    to_train.machines.append(machine)
    database_init.session.commit()

# Remove trainings to a passed User
def remove_training(user_id, machine_id):
    # Check to see if the user is in the database
    to_untrain = is_user_id_present(user_id)
    # If they aren't, leave
    if to_untrain == None:
        raise LookupError(f"User with ID {user_id} does not exist")
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

def change_user_access_level(idnumber, new_access_level):
    result = is_user_id_present(idnumber)
    if result == None:
        raise LookupError(f"User with ID {idnumber} does not exist")
    result.role = new_access_level
    database_init.session.commit()
