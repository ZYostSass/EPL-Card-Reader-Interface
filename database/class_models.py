import base64
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, LargeBinary, Table, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.associationproxy import AssociationProxy
from bcrypt import checkpw, gensalt, hashpw

# Replaced depreciated 'Base = declarative_base()'
class Base(DeclarativeBase):
    pass

class TrainingLog(Base):
    __tablename__ = "training_log"
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    machine_id: Mapped[int] = mapped_column(ForeignKey("machine.id", ondelete="CASCADE"), primary_key=True)
    trained_at: Mapped[datetime] 
    machine: Mapped["Machine"] = relationship(back_populates="trained_users")
    user: Mapped["User"] = relationship(back_populates="training_log")

# User Table:
	# Primary Key: ID Number
	# First Name
	# Last Name
    # Email
    # Role
    # Last Log In datetime
    # List of machines the user is trained on (can be none) -> user_machine assosiation table
<<<<<<< HEAD
=======

class AccessLog(Base):
    __tablename__ = "access_log"
    # Declarative Form, prefered as of SQLAlchemy 2.0
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    checked_in_at: Mapped[datetime.datetime]
    checked_out_at: Mapped[Optional[datetime.datetime]]

    def __init__(self, user_id, checked_in_at, checked_out_at = None):
        self.user_id = user_id
        self.checked_in_at = checked_in_at
        self.checked_out_at = checked_out_at

>>>>>>> 1614586 (Remove unnescessary imports and files, add access log table and stub out access method)
class User(Base):
    __tablename__ = "user"
    # Declarative Form, prefered as of SQLAlchemy 2.0
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    psu_id: Mapped[str]
    badge: Mapped[str]
    firstname: Mapped[str]
    lastname: Mapped[str]
    email: Mapped[str]
    role: Mapped[str]
    pw_hash: Mapped[Optional[str]]
    # List of machines the user is trained on
    training_log: Mapped[List["TrainingLog"]] = relationship(back_populates="user", cascade="all, delete", passive_deletes=True)
    machines: AssociationProxy[List["Machine"]] = association_proxy(
        "training_log",
        "machine",
        creator=lambda machine_obj: TrainingLog(machine=machine_obj, trained_at=datetime.now())
    )
    
    def __init__(self, psu_id, access, fname, lname, email, role, password = None):
        self.psu_id = psu_id
        self.badge = access
        self.firstname = fname
        self.lastname = lname
        self.email = email
        self.training_log = []
        if password is not None and role == "Student":
            raise ValueError("Invalid student configuration")
    
        if password is not None:
            self.pw_hash = hashpw(password, gensalt())
        
        self.role = role
    
    def __repr__(self):
        return f"{self.firstname} {self.lastname} ({self.role})"
    
    def has_admin(self):
        return self.role == "Admin"
    
    def has_manager(self):
        return self.role == "Manager" or self.role == "Admin"
    
    def promote(self, new_role, password):
        if new_role != "Manager" and new_role != "Admin":
            raise ValueError("Invalid role promotion")
        self.role = new_role
        if password is not None:
            self.pw_hash = hashpw(bytes(password, 'utf-8'), gensalt())

machine_tag_association = Table(
    "machine_tag_association",
    Base.metadata,
    Column("machine_id", ForeignKey("machine.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("machine_tag.id", ondelete="CASCADE"), primary_key=True),
)

# Machine Table:
    # Primary Key: ID Number
    # Name
class Machine(Base):
    __tablename__ = "machine"
    # Declarative Form, prefered as of SQLAlchemy 2.0
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    machine_image: Mapped[Optional[bytes]] = mapped_column(LargeBinary, deferred=True, nullable=True) # Lazily load the image
    epl_link: Mapped[Optional[str]] = mapped_column(deferred=True) # Lazily load the link
    # List of Users that are trained on this machine
    trained_users: Mapped[List[TrainingLog]] = relationship(back_populates="machine", cascade="all, delete", passive_deletes=True)
    # Categories associated with each machine
    categories: Mapped[List["MachineTag"]] = relationship(secondary=machine_tag_association, back_populates="machines", cascade="all, delete", passive_deletes=True)
    
    def __init__(self, name, epl_link, file_name = None, machine_image = None):
        self.name = name
        self.epl_link = epl_link
        self.categories = []
        self.trained_users = []
        if file_name is not None and machine_image is not None:
            raise ValueError("Must provide either file_name or machine_image")
        
        if file_name is not None:
            with open(file_name, "rb") as f:
                self.machine_image = base64.b64encode(f.read())
        elif machine_image is not None:
            if not isinstance(machine_image, bytes):
                raise ValueError("machine_image must be of type bytes")
            
            self.machine_image = base64.b64encode(machine_image)
    
    def __repr__(self):
        return self.name
    
    def set_image(self, image: bytes):
        self.machine_image = base64.b64encode(image)

    

class MachineTag(Base):
    __tablename__ = "machine_tag"
    # Declarative Form, prefered as of SQLAlchemy 2.0
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    machines: Mapped[List[Machine]] = relationship(secondary=machine_tag_association, back_populates="categories", cascade="all, delete", passive_deletes=True)
    tag: Mapped[str]
    
    def __init__(self, tag):
        self.tag = tag
        self.machines = []
    
class EventLog(Base):
    __tablename__ = "event_log"
    # Declarative Form, prefered as of SQLAlchemy 2.0
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fname: Mapped[str]
    lname: Mapped[str]
    badge: Mapped[str]
    psu_id: Mapped[str]
    event: Mapped[str]
    timestamp: Mapped[datetime]

    def __init__(self, fname, lname, badge, psu_id, event, timestamp):
        self.fname = fname
        self.lname = lname
        self.badge = badge
        self.psu_id = psu_id
        self.event = event
        self.timestamp = timestamp

    def __repr__(self):
        return f"{self.fname} {self.lname} ({self.badge}) {self.event} at {self.timestamp}"
    
    @staticmethod
    def check_in(user: User):
        return EventLog(user.firstname, user.lastname, user.badge, user.psu_id, "check_in", datetime.now())
    
    @staticmethod
    def check_out(user: User):
        return EventLog(user.firstname, user.lastname, user.badge, user.psu_id, "check_out", datetime.now())
