# Equipment Table (Named after each piece of equipment
	# Foreign Key: ID Number
	# Trained Boolean

import user_db_init
from sqlalchemy import ForeignKey, Column, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Machine(Base):
    __tablename__ = "machine"
    idnumber = Column("ID", Integer, ForeignKey("people.id")) # user_db_init.Person.
    trained = Column("Trained", Boolean)
    
    def __init__(self, idnumber, trained):
        self.idnumber = idnumber
        self.trained = trained
        
    #def __repr__(self) -> str:
    #    return super().__repr__()

    def __repr__(self):
        return f"({self.idnumber} {self.trained})"