from sqlalchemy import create_engine, ForeignKey, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Person(Base):
    __tablename__ = "people"
    idnumber = Column("ID", Integer, primary_key = True)
    firstname = Column("firstname", String)
    lastname = Column("lastname", String)
    
    def __init__(self, idnumber, firstname, lastname):
        self.idnumber = idnumber
        self.firstname = firstname
        self.lastname = lastname

    def __repr__(self) -> str:
        return super().__repr__()