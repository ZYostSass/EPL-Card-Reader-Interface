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
from sqlalchemy import and_, literal_column, select, func, text
from datetime import datetime

# Helper Methods

def process_badge(badge):
    if not isinstance(badge, (str, int)):
        raise ValueError(f"Badge must be a string or integer, not {type(badge)}")

    if isinstance(badge, int):
        badge = str(badge)

    if len(badge) > 6:
        raise ValueError(f"Badge must contain 6 digits, received: {badge}")

    badge = badge.zfill(6)
    return badge

# Checks to see if a given user is in the database, via badge number
# Returns result (either the user or None)
def is_user_badge_present(badge):
    badge = process_badge(badge)
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

def get_machine(id):
    return database_init.session.execute(select(class_models.Machine)
        .where(class_models.Machine.id == id)).scalar_one_or_none()

def get_category(id):
    return database_init.session.execute(select(class_models.MachineTag)
        .where(class_models.MachineTag.id == id)).scalar_one_or_none()


# Universal Commands

# Takes parsed card data and inputs it into the database
# Returns either a LookupError or the User
# Can be used to access User members
def checkin_user(badge):
    badge = process_badge(badge)
    # Checks to see if the user is in the database
    user = is_user_badge_present(badge)
    # If not, leave
    if user == None:
        raise LookupError(f"User with access number {badge} does not exist")
    
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

class DisplayAccessLog:
    user: class_models.User
    time_in: datetime
    time_out: Optional[datetime]

    def __init__(self, user, time_in, time_out):
        self.user = user
        self.time_in = time_in
        self.time_out = time_out

# Gets the first name, last name, and id number of a given badge number
# Returns either None or the entire User
def get_user(badge):
    badge = process_badge(badge)
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
        raise ValueError(f"User with {id} is not in the database")
    return user

def get_int_key(key): 
    try:
        value =  database_init.session.execute(select(class_models.KeyValue)
            .where(class_models.KeyValue.key == key)).scalar_one_or_none()
        return int(value.value)
    except:
        return None
    


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
    badge_number = badge_number.zfill(6)
    # Looks for the User with a matching ID
    to_delete = is_user_badge_present(badge_number)
    # If not found, return
    if to_delete is None:
        raise ValueError(f"User with badge {badge_number} does not exist")
    # Else, remove from the database
    else:
        database_init.session.delete(to_delete)
        database_init.session.commit()

# Update user's information 
def update_user_option(id, badge, fname, lname, email):
    user = get_user(badge)
    if user is not None:
        user.psu_id = id
        user.badge = badge
        user.firstname = fname
        user.lastname = lname
        user.email = email
        database_init.session.commit()
    else:
        raise ValueError("User doesn not exist")

def all_categories():
    return database_init.session.execute(select(class_models.MachineTag)).scalars().all()

def uncategorized_machines():
    subq = select(literal_column("machine_id")).select_from(text("machine_tag_association"))
    return database_init.session.execute(select(class_models.Machine).where(class_models.Machine.id.not_in(subq))).scalars().all()

def uncategorized_machines_without_user(user_id):
    subq_machines = select(literal_column("machine_id")).select_from(text("machine_tag_association"))
    subq_user_machines = select(class_models.TrainingLog.machine_id).where(class_models.TrainingLog.user_id == user_id)
    return database_init.session.execute(select(class_models.Machine).where(and_(class_models.Machine.id.not_in(subq_machines), class_models.Machine.id.not_in(subq_user_machines)))).scalars().all()


# Add new machines to the database
def add_machine(name, link, categories, img):
    print(img)
    if img is not None and img.filename != "":
        img = img.read()
        print(type(img))
        machine = class_models.Machine(name=name, epl_link=link, machine_image=img)
    else:
        machine = class_models.Machine(name=name, epl_link=link)
    for category in categories:
        if category is not None:
            machine.categories.append(get_category(category))

    database_init.session.add(machine)
    database_init.session.commit()

# Edit a given machine's name
def edit_machine(id, name, link, categories, img):
    # Check to see if the machine is already in the database
    machine = get_machine(id)
    
    if machine == None:
        raise LookupError(f"Machine with id {id} does not exist")

    machine.name = name
    machine.epl_link = link

    machine.categories.clear()
    for category in categories:
        if category is not None:
            machine.categories.append(get_category(category))

    if img is not None and img.filename != "":
        machine.set_image(img.read())

    database_init.session.commit()

# Remove a machine from the database
def remove_machine(id):
    # Check to see if the machine is already in the database
    machine = get_machine(id)
    # If it is, leave
    if machine == None:
        raise LookupError(f"Machine with id {id} does not exist")
    database_init.session.delete(machine)
    database_init.session.commit()

def update_category_by_id(id, name):
    category = get_category(id)

    if category == None:
        raise LookupError(f"Category with id {id} does not exist")
    
    category.tag = name

    database_init.session.commit()


def insert_category_name(name):
    category = class_models.MachineTag(tag=name)
    database_init.session.add(category)
    database_init.session.commit()

# Remove a machine from the database
def remove_category_by_id(id):
    # Check to see if the machine is already in the database
    category = get_category(id)
    # If it is, leave
    if category == None:
        raise LookupError(f"Category with id {id} does not exist")
    database_init.session.delete(category)
    database_init.session.commit()

# Add trainings to a passed User
def add_training(badge, machine_id):
    badge = process_badge(badge)
    # Check to see if the user is in the database
    to_train = get_user(badge)
    # If they aren't, leave
    if to_train == None:
        raise LookupError(f"User with ID {badge} does not exist")
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
    user_badge = process_badge(user_badge)
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
    new_badge = process_badge(new_badge)
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