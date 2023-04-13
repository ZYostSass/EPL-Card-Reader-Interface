# User Table:
	# Primary Key: ID Number
	# Badge Number
	# First Name
	# Last Name
	# Emergency Contact Info
	# User Level (Admin, Manager, Student)

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase #, Mapped, mapped_column, relationship

# Replaced depreciated 'Base = declarative_base()'
class Base(DeclarativeBase):
    pass

# -- User Base Class --

class User(Base):
    __tablename__ = "users"

    # Imperative Approach
    idnumber = Column("ID", Integer, primary_key = True)
    accessnumber = Column("Access ID", Integer)
    # Strings corispond to VARCHARS from SQL, thus a size is needed
    # Characters: Admin(5), Manager(7), Student(7)
    role = Column("role", String(7))
    # 50 characters seemded ample, but may be expanded if needed
    firstname = Column("firstname", String(50))
    lastname = Column("lastname", String(50))

    # Declarative Approach
    #idnumber: Mapped[int] = mapped_column(primary_key=True)
    #accessnumber: Mapped[int] = mapped_column(int)
    #role: Mapped[str] = mapped_column(String(7))
    #firstname: Mapped[str] = mapped_column(String(50))
    #lastname: Mapped[str] = mapped_column(String(50))

    def __init__(self, idnumber, accessnumber, role, firstname, lastname):
        self.idnumber = idnumber
        self.accessnumber = accessnumber
        self.role = role
        self.firstname = firstname
        self.lastname = lastname

    def __repr__(self) -> str:
        return f"User(idnumber={self.idnumber!r}, accessnumer={self.accessnumber!r}, role={self.role!r}, firstname={self.firstname!r}, lastname={self.lastname!r})"

# -- Machine Base Class --

# Equipment Table (Named after each piece of equipment
	# Foreign Key(User.idnumber): ID Number
	# Trained Boolean

class Machine(Base):
    __tablename__ = "machine"

    # Imperative Approach
    idnumber = Column("ID", Integer, ForeignKey(User.idnumber), primary_key = True)
    trained = Column("Trained", Boolean)

    # Declarative Approach
    #idnumber: Mapped[int] = mapped_column(ForeignKey(User.idnumber), primary_key=True)
    #trained: Mapped[Boolean] = mapped_column(bool)

    def __init__(self, idnumber, trained):
        self.idnumber = idnumber
        self.trained = trained
        
    def __repr__(self) -> str:
        return f"Machine(idnumber={self.idnumber!r}, trained={self.trained!r})"