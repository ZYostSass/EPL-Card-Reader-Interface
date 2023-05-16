# Students can only log in and out using their ID card via the scanner
# Managers can:
	# Do everything a Student can
	# Add new Students to the tables
	# Change a Student's training on a given machine
	# NOT required to be trained on all machines
# Admins can:
	# Do everything a Manager can do
	# Change a user's access level

from . import database_init
from . import class_models
from sqlalchemy import select, func

# Universal Commands

# Takes parsed card data and inputs it into the database
def checkin_user(badge):
    to_checkin = database_init.session.execute(select(class_models.User)
        .where(class_models.User.badge == badge)).scalar_one_or_none()
    if to_checkin == None:
        print("User is not in the database")
        return
    #print("Welcome", to_checkin)
    return to_checkin

def get_user_data(badge):
    to_display = database_init.session.execute(select(class_models.User)
        .where(class_models.User.badge == badge)).scalar_one_or_none()
    if to_display == None:
        print("User is not in the database")
        return
    return [to_display.firstname, to_display.lastname, to_display.id]

# Manager Commands

# Addes a new user, if the ID is not currently present    
def add_new_user(idnumber, access, firstname, lastname, email, role):
    # Check if user already exists
    to_check = database_init.session.execute(select(class_models.User)
        .where(class_models.User.id == idnumber)).scalar_one_or_none()
    # Raise an exception if they do
    if to_check != None:
        raise ValueError(f"User with ID {idnumber} is already in the database")
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
        raise LookupError(f"User with ID {idnumber} does not exist")
    # Else, remove from the database
    else:
        database_init.session.delete(to_delete)
        database_init.session.commit()

# Add new machines to the database
def add_machine (name):
    # Check to see if the machine is already in the database
    machine = database_init.session.execute(select(class_models.Machine)
        .where(class_models.Machine.name == name)).scalar_one_or_none()
    # If it is, leave
    if machine is not None:
        raise ValueError("Machine is already in the database")
    
    # Otherwise, add it to the end of the database
    max_id = database_init.session.query(func.max(class_models.Machine.id)).scalar()
    next_id = (max_id or 0) + 1

    to_add = class_models.Machine(next_id, name)
    database_init.session.add(to_add)
    database_init.session.commit()

# Edit a given machine's name
def edit_machine(name, new_name):
    # Check to see if the machine is already in the database
    machine = database_init.session.execute(select(class_models.Machine)
        .where(class_models.Machine.name == name)).scalar_one_or_none()
    # If it isn't, leave
    if machine == None:
        print("Machine isn't in the database")
        return
    # Otherwise, edit it
    machine.name = new_name
    database_init.session.commit()

# Remove a machine from the database
def remove_machine(name):
    # Check to see if the machine is already in the database
    machine = database_init.session.execute(select(class_models.Machine)
        .where(class_models.Machine.name == name)).scalar_one_or_none()
    # If it is, leave
    if machine is None:
        raise ValueError(f"Machine is not in the database")
    database_init.session.delete(machine)
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
    to_delete = database_init.session.execute(select(class_models.User)
        .where(class_models.User.id == user_id)).scalar_one_or_none()
    # If they aren't, leave
    if to_delete == None:
        print("User is not in the database")
        return
    # Else, remove from the database
    database_init.session.delete(to_delete)
    database_init.session.commit()

# Output all Machines and user trained on them
def read_all_machines():
    # Current as of SQLAlchemy 2.0
    # TODO - Display all users trained
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

# Unused and an artifact from prior development
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

# Test: Returning all equipment data
def read_all_machines():
    results = database_init.session.scalars(select(class_models.Machine)).all()
    return results