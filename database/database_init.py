import os.path
import class_models

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

path = os.getcwd
# print(path)
check_file = os.path.isfile("database.db") #path + 
if not (check_file):
    # If database files don't exist
    # Create a base version
    # Create the first entry as an Admin

    # Initialize Session
    engine = create_engine("sqlite:///database.db")
    class_models.Base.metadata.create_all(engine)
    Session = sessionmaker(engine)
    session = Session()

    # Create Base Admin
    # TODO - Fill in correct info
    base_admin = class_models.User(0, 0, "Admin", "John", "Doe")
    session.add(base_admin)
    session.commit()
    # Set Base Admin Machines to False
    machine_admin = class_models.Machine(0, 0)
    session.add(machine_admin)
    session.commit()
    
else:
    # Otherwise
    # Load the files into memory
    engine = create_engine("sqlite:///database.db")
    class_models.Base.metadata.create_all(engine)
    Session = sessionmaker(engine)
    session = Session()

    print("Files Found")

# TODO - Format for Flask
# "sqlite:///mydb.db"
# New user has all training set to False
# Admins can edit info as needed
# Check to see if table file is present
# Last login