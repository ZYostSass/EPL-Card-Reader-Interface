# User Table:
	# Primary Key: ID Number
	# Badge Number
	# First Name
	# Last Name
	# Emergency Contact Info
	# User Level (Admin, Manager, Student)

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase

# Replaced depreciated 'Base = declarative_base()'
class Base(DeclarativeBase):
    pass

# -- User Base Class --

class User(Base):
    __tablename__ = "users"
    idnumber = Column("ID", Integer, primary_key = True)
    accessnumber = Column("Access ID", Integer)
    # Strings corispond to VARCHARS from SQL, thus a size is needed
    # Characters: Admin(5), Manager(7), Student(7)   
    role = Column("role", String(7))
    # 50 characters seemded ample, but may be expanded if needed
    firstname = Column("firstname", String(50))
    lastname = Column("lastname", String(50))
        
    def __init__(self, idnumber, accessnumber, role, firstname, lastname):
        self.idnumber = idnumber
        self.accessnumber = accessnumber
        self.role = role
        self.firstname = firstname
        self.lastname = lastname

    def __repr__(self):
        return f"({self.idnumber} {self.accessnumber} {self.role} {self.firstname} {self.lastname})"

# -- Machine Base Class --

# Equipment Table (Named after each piece of equipment
	# Foreign Key(User.idnumber): ID Number
	# Trained Boolean

class Machine(Base):
    __tablename__ = "machine"
    idnumber = Column("ID", Integer, ForeignKey(User.__tablename__), primary_key = True)
    trained = Column("Trained", Boolean)
    
    def __init__(self, idnumber, trained):
        self.idnumber = idnumber
        self.trained = trained
        
    def __repr__(self):
        return f"({self.idnumber} {self.trained})"