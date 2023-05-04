import os.path
from database import class_models

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

path = os.getcwd
# print(path)
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
    base_admin = class_models.User(0, 0, "John", "Doe", "jdoe@pdx.edu", "Admin")
    session.add(base_admin)
    session.commit()

    # Add all machines to database

    # Circuit Board Manufacturing

    # LPFK S63 PCB Router
    machine0 = class_models.Machine(0, "LPFK S63 PCB Router")
    session.add(machine0)
    session.commit()
    # LPKF S104 PCB Router
    machine1 = class_models.Machine(1, "LPKF S104 PCB Router")
    session.add(machine1)
    session.commit()
    # LPKF Multipress S
    machine2 = class_models.Machine(2, "LPKF Multipress S")
    session.add(machine2)
    session.commit()
    # T200N Desktop Solder Oven
    machine3 = class_models.Machine(3, "T200N Desktop Solder Oven")
    session.add(machine3)
    session.commit()
    # Pick and Place
    machine4 = class_models.Machine(4, "Pick and Place")
    session.add(machine4)
    session.commit()
    # Soldering Equipment
    machine5 = class_models.Machine(5, "Soldering Equipment")
    session.add(machine5)
    session.commit()
    # Test and Measurement
    machine6 = class_models.Machine(6, "Test and Measurement")
    session.add(machine6)
    session.commit()

    # 3D Printers

    # Ultimaker3 Extended 3D Printer
    machine7 = class_models.Machine(7, "Ultimaker3 Extended 3D Printer")
    session.add(machine7)
    session.commit()
    # Form 3 SLA Printer
    machine8 = class_models.Machine(8, "Form 3 SLA Printer")
    session.add(machine8)
    session.commit()

    # Machining Equipment

    # Little Machine Shop Mill
    machine9 = class_models.Machine(9, "Little Machine Shop Mill")
    session.add(machine9)
    session.commit()
    # Little Machine Shop Lathe
    machine10 = class_models.Machine(10, "Little Machine Shop Lathe")
    session.add(machine10)
    session.commit()
    # Drill Press
    machine11 = class_models.Machine(11, "Drill Press")
    session.add(machine11)
    session.commit()
    # WAZER
    machine12 = class_models.Machine(12, "WAZER")
    session.add(machine12)
    session.commit()

    # Laser Cutters

    # QD-1390 Laser Cutter
    machine13 = class_models.Machine(13, "QD-1390 Laser Cutter")
    session.add(machine13)
    session.commit()


    # Miscellaneous

    # Thermocut 115/E
    machine13 = class_models.Machine(13, "Thermocut 115/E")
    session.add(machine13)
    session.commit()
    # Silhouette Cameo
    machine14 = class_models.Machine(14, "Silhouette Cameo")
    session.add(machine14)
    session.commit()
    # EZFORM SV 1217
    machine15 = class_models.Machine(15, "EZFORM SV 1217")
    session.add(machine15)
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