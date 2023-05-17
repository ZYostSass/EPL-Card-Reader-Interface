import os.path
import class_models

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

path = os.getcwd
check_file = os.path.isfile("database.db") 
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
    base_admin = class_models.User(0, 0, "John", "Doe", "jdoe@pdx.edu", "Admin", class_models.datetime.datetime.now())
    session.add(base_admin)
    session.commit()

    # Add all machines to database

    # Circuit Boards

    # OSH Park
    machine0 = class_models.Machine(0, "OSH Park")
    session.add(machine0)
    # OSH Stencils
    machine1 = class_models.Machine(1, "OSH Stencils")
    session.add(machine1)
    #JLCPCB
    machine2 = class_models.Machine(2, "JLCPCB")
    session.add(machine2)
    # 4PCB
    machine3 = class_models.Machine(3, "4PCB")
    session.add(machine3)
    
    # Electronic Comnponents

    # Digikey
    machine4 = class_models.Machine(4, "Digikey")
    session.add(machine4)
    # Mouser
    machine5 = class_models.Machine(5, "Mouser")
    session.add(machine5)

    # 3D Parts
    
    # Rapidmade
    machine6 = class_models.Machine(6, "Rapidmade")
    session.add(machine6)
    # Protolabs
    machine7 = class_models.Machine(7, "Protolabs")
    session.add(machine7)
    # 3D Hubs
    machine8 = class_models.Machine(8, "3D Hubs")
    session.add(machine8)
    # Xometry
    machine9 = class_models.Machine(9, "Xometry")
    session.add(machine9)

    # Mechanical Components
    
    # McCaster-Carr
    machine10 = class_models.Machine(10, "McCaster-Carr")
    session.add(machine10)
    # MSC Direct
    machine11 = class_models.Machine(11, "MSC Direct")
    session.add(machine11)
    # Metal Supermarkets
    machine12 = class_models.Machine(12, "Metal Supermarkets")
    session.add(machine12)
    # TAP Plastics
    machine13 = class_models.Machine(13, "TAP Plastics")
    session.add(machine13)

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
# New user has all training set to False
# Admins can edit info as needed
# Last login