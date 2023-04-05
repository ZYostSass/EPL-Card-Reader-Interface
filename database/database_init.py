import os.path
import user_db_init
import machine_db_init

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

path = os.getcwd
check_file = os.path.isfile(path + '/user.db')
print(check_file)

# If database files don't exist
# create a base version
# Create the first entry as an Admin

# Otherwise
# Load the files into memory

# TODO - Format for Flask
# "sqlite:///mydb.db"

Base = declarative_base()

engine = create_engine("sqlite:///mydb.db")

Base.metadata.create_all(bind = engine)

Session = sessionmaker(bind = engine)
session = Session()

# Example of Entry
person = user_db_init.Person(234324, 910221, "Admin", "John", "Doe")
# New user has all training set to False
# Admins can edit info as needed
# Check to see if table file is present
# Last login
session.add(person)
session.commit()

# Queries
results = session.query(user_db_init.Person).all()
print(results)