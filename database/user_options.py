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

# Universal Commands

# Takes parsed card data and inputs it into the database
def checkin_user(idnumber):
    print("Hello")
    
# Manager Commands
    
def add_new_user(idnumber, accesnumber, firstname, lastname):
    print("Hello")
    
def user_check(firstname, lastname):
    print("Hello")
    
def change_user_training(idnumber, machine, trained_status):
    print("Hello")

# Admin Commands

def chance_user_access_level(idnumber):
    print("Hello")