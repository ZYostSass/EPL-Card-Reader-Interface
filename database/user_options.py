"""
The access control system allows different user roles with varying permissions.

- Students can only log in and out using their ID card via the scanner.

- Managers have the following capabilities:
    - Perform all actions that a Student can do.
    - Add new Students to the tables.
    - Change a Student's training on a given machine.
    - Managers are not required to be trained on all machines.

- Admins have the following capabilities:
    - Perform all actions that a Manager can do.
    - Change a user's access level.

"""

from typing import Optional
from bcrypt import checkpw
from . import database_init
from . import class_models
from sqlalchemy import select, func
from datetime import datetime

def is_user_badge_present(badge):
    """
    Checks if a user with the given badge number is present in the database.

    Args:
        badge (str): The badge number of the user.

    Returns:
        User or None: The user object if found, None otherwise.

    """

    return database_init.session.execute(select(class_models.User)
        .where(class_models.User.badge == badge)).scalar_one_or_none()

def is_user_id_present(psu_id):
    """
    Checks to see if a given user is in the database, via PSU ID.
    Returns result (either the user or None).
    """

    return database_init.session.execute(select(class_models.User)
        .where(class_models.User.psu_id == psu_id)).scalar_one_or_none()

def is_machine_present(name):
    """
    Checks to see if a given machine is in the database, via name.
    Returns result (either the user or None).
    """

    return database_init.session.execute(select(class_models.Machine)
        .where(class_models.Machine.name == name)).scalar_one_or_none()

"""
Universal Commands
"""

def checkin_user(badge):
    """
    Takes parsed card data and inputs it into the database.
    Returns either None or the User.
    Can be used to access User members.
    """

    user = is_user_badge_present(badge)
    if user == None:

        raise LookupError(f"User with access number {badge} does not exist")
    
    log = class_models.EventLog.check_in(user)
    database_init.session.add(log)
    database_init.session.commit()
    
    return user

def access_logs():
    """
    Returns all access logs from the database.
    """

    return database_init.session.execute(select(class_models.EventLog)).scalars().all()

def get_user(badge):
    """
    Gets the first name, last name, and ID number of a given badge number.
    Returns either None or the entire User.
    """

    to_display = is_user_badge_present(badge)
    if to_display == None:

        return None

    else:
        return to_display

def get_user_by_psu_id(id): 
    """
    Retrieves a user from the database based on their PSU ID.
    Returns the user if found, otherwise raises an error.
    """

    user = database_init.session.execute(select(class_models.User)
        .where(class_models.User.psu_id == id)).scalar_one_or_none()
    
    if user == None:

        raise ValueError(f"User with PSU ID {id} is not in the database")
    
    return user

def get_user_by_id(id): 
    """
    Retrieves a user from the database based on their ID.
    Returns the user if found, otherwise raises an error.
    """

    user = database_init.session.execute(select(class_models.User)                                  
        .where(class_models.User.id == id)).scalar_one_or_none() 
    
    if user == None:

        raise ValueError(f"User with ID {id} is not in the database")
    
    return user

def check_user_password(email, password):
    """
    Checks the provided email and password against the database.
    Returns the user if the credentials are valid, otherwise raises an error.
    """

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

"""
Manager Commands
"""

def add_new_user(psu_id, access, firstname, lastname, email, role):
    """
    Adds a new user to the database if the ID is not currently present.

    """

    to_check = is_user_id_present(psu_id)
    if to_check != None:

        raise ValueError(f"User with ID {psu_id} is already in the database")
    
    user = class_models.User(psu_id, access, firstname, lastname, email, role)
    database_init.session.add(user)
    database_init.session.commit()

def remove_user(idnumber):
    """
    Removes a user from the database if they are present.
    If the PSUID is not in the database, will throw a ValueError.
    Otherwise uses the built-in session.delete functionality.
    to_delete is assigned base on the helper is_user_id_present helper function.
    """

    to_delete = is_user_id_present(idnumber)
    if to_delete is None:

        raise ValueError(f"User with PSU ID {idnumber} does not exist")
    
    else:
        database_init.session.delete(to_delete)
        database_init.session.commit()

def add_machine(name):
    """
    Adds a new machine to the database if it is not already present.
    """

    machine = is_machine_present(name)
    if machine != None:

        raise ValueError(f"{name} is already in the database")
    
    max_id = database_init.session.query(func.max(class_models.Machine.id)).scalar()
    next_id = (max_id or 0) + 1
    to_add = class_models.Machine(next_id, name)
    database_init.session.add(to_add)
    database_init.session.commit()

def edit_machine(name, new_name):
    """
    Edits the name of a given machine.
    """

    machine = is_machine_present(name)
    if machine == None:

        raise LookupError(f"Machine with name {name} does not exist")
    
    machine.name = new_name
    database_init.session.commit()

def remove_machine(name):
    """
    Removes a machine from the database if it is present.
    """

    machine = is_machine_present(name)
    if machine == None:

        raise LookupError(f"Machine with name {name} does not exist")
    
    database_init.session.delete(machine)
    database_init.session.commit()

def add_training(user_id, machine_id):
    """
    Adds a training for a user on a given machine.
    """

    to_train = is_user_id_present(user_id)
    if to_train == None:

        raise LookupError(f"User with ID {user_id} does not exist")
    
    machine = database_init.session.execute(select(class_models.Machine)
        .where(class_models.Machine.id == machine_id)).scalar_one_or_none()
    
    if machine == None:

        raise LookupError(f"Machine with ID {machine_id} does not exist")
    
    to_train.machines.append(machine)
    database_init.session.commit()

def remove_training(user_id, machine_id):
    """
    Removes a training for a user on a given machine.
    """

    to_untrain = is_user_id_present(user_id)
    if to_untrain == None:

        raise LookupError(f"User with ID {user_id} does not exist")
    
    machine = database_init.session.execute(select(class_models.Machine)
        .where(class_models.Machine.id == machine_id)).scalar_one_or_none()
    
    if machine == None:

        raise LookupError(f"Machine with ID {machine_id} does not exist")
    
    to_untrain.machines.remove(machine)
    database_init.session.commit()

def read_all_machines():
    """
    Returns a list of all machines in the database.
    """

    results = database_init.session.scalars(select(class_models.Machine)).all()
    return results

def read_all():
    """
    Returns a list of all users in the database.
    """

    results = database_init.session.scalars(select(class_models.User)).all()
    return results

def edit_user_badge(idnumber, new_badge):
    """
    Edits the badge number of a user.
    """

    to_edit = is_user_id_present(idnumber)
    if to_edit is None:

        raise ValueError(f"User with PSU ID {idnumber} does not exist")
    
    to_edit.badge = new_badge
    database_init.session.commit()

def edit_user_name(idnumber, new_first, new_last):
    """
    Edits the name of a user.
    """

    to_edit = is_user_id_present(idnumber)
    if to_edit is None:

        raise ValueError(f"User with PSU ID {idnumber} does not exist")
    
    to_edit.firstname = new_first
    to_edit.lastname = new_last
    database_init.session.commit()

def edit_user_email(idnumber, new_email):
    """
    Edits the email of a user.
    """

    to_edit = is_user_id_present(idnumber)
    if to_edit is None:

        raise ValueError(f"User with PSU ID {idnumber} does not exist")
    
    to_edit.email = new_email
    database_init.session.commit()

def read_all_online():
    """
    Returns a list of all users currently in the lab.
    """

    results = database_init.session.scalars(select(class_models.User)).all()
    return results

"""
Admin Commands
"""

def change_user_access_level(idnumber, new_access_level, password):
    """
    Changes the access level of a user.
    
    param: idnumber is the PSUID, new_access_level is 'Manager' or 'Admin'
    will require the newly assigned user to create a password for future use.
    """

    user = is_user_id_present(idnumber)
    if user == None:

        raise LookupError(f"User with ID {idnumber} does not exist")
    
    if password is None and user.pw_hash is None:

        raise ValueError("User does not have a password, please provide one")
    
    user.promote(new_access_level, password)
    database_init.session.commit()

def purge_database():
    """
    Purges the database of all users and machines.
    """

    class_models.Base.metadata.drop_all()