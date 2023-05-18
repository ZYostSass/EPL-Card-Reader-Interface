import datetime
from typing import Optional
from sqlalchemy import Column, Table, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from bcrypt import checkpw, gensalt, hashpw

# Replaced depreciated 'Base = declarative_base()'
class Base(DeclarativeBase):
    pass

# Bi-directional join table for many-to-many relationships
# using sqlalchemy.Column construct
    # Primary Key: User ID -> user.id
    # Primary Key: Machine ID -> machine.id
user_machine_join_table = Table(
    "user_machine_table",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("machine_id", ForeignKey("machine.id"), primary_key=True),
)

# User Table:
	# Primary Key: ID Number
	# First Name
	# Last Name
    # Email
    # Role
    # Last Log In datetime
    # List of machines the user is trained on (can be none) -> user_machine assosiation table

class User(Base):
    __tablename__ = "user"
    # Declarative Form, prefered as of SQLAlchemy 2.0
    id: Mapped[int] = mapped_column(primary_key=True)
    badge: Mapped[int]
    firstname: Mapped[str]
    lastname: Mapped[str]
    email: Mapped[str]
    role: Mapped[str]
    pw_hash: Mapped[str]
    last_login: Mapped[datetime.datetime]
    # List of machines the user is trained on
    machines: Mapped[Optional[list["Machine"]]] = relationship(secondary = user_machine_join_table, back_populates="trained_users")
    
    def __init__(self, id, access, fname, lname, email, role, last_login, password):
        self.id = id
        self.badge = access
        self.firstname = fname
        self.lastname = lname
        self.email = email
        self.pw_hash = hashpw(password, gensalt())
        self.role = role
        self.last_login = last_login
    
    def __repr__(self):
        return f"{self.firstname} {self.lastname}"

# Machine Table:
    # Primary Key: ID Number
    # Name
    # Trained Users list (can be none) -> user_machine assosiation table
class Machine(Base):
    __tablename__ = "machine"
    # Declarative Form, prefered as of SQLAlchemy 2.0
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    # List of Users that are trained on this machine
    trained_users: Mapped[Optional[list["User"]]] = relationship(secondary = user_machine_join_table, back_populates="machines")
    
    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    def __repr__(self):
        return self.name

# Holding off on deleting this for now
"""    
class UserMachine(Base):
    __tablename__ = "usermachine"
    # Declarative Form, prefered as of SQLAlchemy 2.0
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped["User"] = mapped_column(ForeignKey("user.id")), relationship(back_populates="user.id")
    #machine_id: Mapped[int] = mapped_column(ForeignKey("machine.id"))
    last_trained: Mapped[datetime.datetime]

    # Imperative Form, legacy since SQLAlchemy 1.4
    #id = Column(Integer, primary_key=True)
    #student_id = Column(Integer, ForeignKey('student.id'))
    #machine_id = Column(Integer, ForeignKey('machine.id'))
    #last_trained = Column(datetime.datetime)
    
    def __init__(self, student, machine, date):
        self.student = student
        self.machine = machine
        self.last_trained = date
    
    def __repr__(self):
        return f"{self.student} was last trained on {self.machine} on {self.last_trained}"
    
# Define the association table for the many-to-many relationship between Student and Machine
# This is equivalent to defining the UserMachine class
#students_machines = Table('students_machines',
    #Column('student_id', Integer, ForeignKey('student.id'), primary_key=True),
    #Column('machine_id', Integer, ForeignKey('machine.id'), primary_key=True)
#)

#training = StudentMachine(student=student1, machine=machine2, date=datetime.now())
#student1.trainings.append(training)
#machine2.trainings.append(training)
"""