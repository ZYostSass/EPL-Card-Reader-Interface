from sqlalchemy import create_engine, ForeignKey, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Person(Base):
    __tablename__ = "people"
    idnumber = Column("ID", Integer, primary_key = True)
    firstname = Column("firstname", String)
    lastname = Column("lastname", String)
    # Pointer to array with trained boolean?
    # Admin, Manager, Student
    
    def __init__(self, idnumber, firstname, lastname):
        self.idnumber = idnumber
        self.firstname = firstname
        self.lastname = lastname

    #def __repr__(self) -> str:
    #    return super().__repr__()

    def __repr__(self):
        return f"({self.idnumber} {self.firstname} {self.lastname})"
    
# TODO - Format for Flask
# "sqlite:///mydb.db"
engine = create_engine("sqlite:///mydb.db", echo = True)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# Example of Entry
person = Person(234324, "John", "Doe")
# New user has all training set to False
# Admins can edit info as needed
# Check to see if table file is present
# Last login
session.add(person)
session.commit()

# Queries
results = session.query(Person).all()
print(results)

#