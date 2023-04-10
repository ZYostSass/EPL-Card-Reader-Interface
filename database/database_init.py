import os.path
import user_db_init
import machine_db_init

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

path = os.getcwd
check_file = os.path.isfile("users.db") #path + 
if not (check_file):
    # If database files don't exist
    # Create a base version
    # Create the first entry as an Admin

    # Initialize Session
    
    # Depreciated - TODO: Replace
    user_base = declarative_base()

    users_engine = create_engine("sqlite:///users.db")
    user_base.metadata.create_all(bind = users_engine)
    Session = sessionmaker(bind = users_engine)
    session = Session()

    # Create Base Admin
    base_admin = user_db_init.User(0, 0, "Admin", "John", "Doe")
    session.add(base_admin)
    session.commit()
else:
    # Otherwise
    # Load the files into memory
    print("Files Found")

# TODO - Format for Flask
# "sqlite:///mydb.db"
# New user has all training set to False
# Admins can edit info as needed
# Check to see if table file is present
# Last login