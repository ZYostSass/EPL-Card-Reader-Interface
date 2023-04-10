# User Table:
	# Primary Key: ID Number
	# Badge Number
	# First Name
	# Last Name
	# Emergency Contact Info
	# User Level (Admin, Manager, Student)

from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

# Depreciated - TODO: Replace
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    idnumber = Column("ID", Integer, primary_key = True)
    accessnumber = Column("Access ID", Integer)   
    role = Column("role", String)
    firstname = Column("firstname", String)
    lastname = Column("lastname", String)
        
    def __init__(self, idnumber, accessnumber, role, firstname, lastname):
        self.idnumber = idnumber
        self.accessnumber = accessnumber
        self.role = role
        self.firstname = firstname
        self.lastname = lastname

    #def __repr__(self) -> str:
    #    return super().__repr__()

    def __repr__(self):
        return f"({self.idnumber} {self.accessnumber} {self.role} {self.firstname} {self.lastname})"
    