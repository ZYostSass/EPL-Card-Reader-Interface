import os.path
from database import class_models

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


path = os.getcwd()
# print(path)
check_file = os.path.isfile("database.db")
if not (check_file):
    prefix = "web_app/static/"
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
    base_admin = class_models.User(
        psu_id="900000000", access="000001", fname="John",
        lname="Admin", email="jadmin@pdx.edu", password=b"password", role="Admin")
    session.add(base_admin)

    base_manager = class_models.User(
        psu_id="900000001", access="000002", fname="John",
        lname="Manager", email="jmanager@pdx.edu", password=b"password", role="Manager")
    session.add(base_manager)

    student1 = class_models.User(psu_id="900000011", access="000011", fname="John", lname="Student", email="jstudent@pdx.edu", password=None, role="Student")
    session.add(student1)
    student2 = class_models.User(
        psu_id="900000012", access="000012", fname="Frank",
        lname="Student", email="fstudent@pdx.edu", password=None, role="Student")
    session.add(student2)
    student3 = class_models.User(
        psu_id="900000013", access="000013", fname="Emily",
        lname="Student", email="estudent@pdx.edu", password=None, role="Student")
    session.add(student3)
    session.commit()

    event_log11 = class_models.EventLog(
        fname=student1.firstname, lname=student1.lastname, badge=student1.badge,
        psu_id=student1.psu_id, event="check_in", timestamp=datetime.now() - timedelta(hours=1))
    session.add(event_log11)
    event_log12 = class_models.EventLog(
        fname=student1.firstname, lname=student1.lastname,
        badge=student1.badge, psu_id=student1.psu_id, event="check_out", timestamp=datetime.now())
    session.add(event_log12)

    event_log21 = class_models.EventLog(
        fname=student1.firstname, lname=student1.lastname, badge=student1.badge,
        psu_id=student1.psu_id, event="check_in", timestamp=datetime.now() - timedelta(hours=2, minutes=5))
    session.add(event_log21)
    event_log22 = class_models.EventLog(
        fname=student1.firstname, lname=student1.lastname, badge=student1.badge,
        psu_id=student1.psu_id, event="check_out", timestamp=datetime.now() - timedelta(hours=2))
    session.add(event_log22)

    event_log31 = class_models.EventLog(
        fname=student2.firstname, lname=student2.lastname, badge=student2.badge,
        psu_id=student2.psu_id, event="check_in", timestamp=datetime.now() - timedelta(hours=1, minutes=5))
    session.add(event_log31)
    event_log32 = class_models.EventLog(
        fname=student2.firstname, lname=student2.lastname, badge=student2.badge,
        psu_id=student2.psu_id, event="check_out", timestamp=datetime.now() - timedelta(minutes=5))
    session.add(event_log32)

    event_log41 = class_models.EventLog(fname=student3.firstname, lname=student3.lastname, badge=student3.badge,
                                        psu_id=student3.psu_id, event="check_in", timestamp=datetime.now() - timedelta(hours=1))
    session.add(event_log41)
    event_log42 = class_models.EventLog(fname=student3.firstname, lname=student3.lastname,
                                        badge=student3.badge, psu_id=student3.psu_id, event="check_out", timestamp=datetime.now())
    session.add(event_log42)
    
    session.commit()

    # Add all machines to database

    # Circuit Board Manufacturing
    circuit_board_manufacturing = class_models.MachineTag("Circuit Board Manufacturing")

    # LPKF Multipress S
    machine0 = class_models.Machine(
        "LPKF Multipress S",
        "https://psu-epl.github.io/doc/equip/misc/LPKF_MultipressS/",
        file_name=(prefix + "equipment_images/circuit_board_manufacturing/lpkf_multipress_s.jpg")
    )
    machine0.categories.append(circuit_board_manufacturing)
    student1.machines.append(machine0)
    session.add(machine0)
    session.commit()

    # LPFK S63 PCB Router
    machine1 = class_models.Machine(
        "LPKF S63 PCB Router",
        "https://psu-epl.github.io/doc/equip/router/LPKF/",
        file_name=(prefix + "equipment_images/circuit_board_manufacturing/lpkf_s63_pcb_router.jpg")
    )
    machine1.categories.append(circuit_board_manufacturing)
    session.add(machine1)
    session.commit()

    # LPKF S104 PCB Router
    machine2 = class_models.Machine(
        "LPKF S104 PCB Router",
        "https://psu-epl.github.io/doc/equip/router/LPKF_S104/",
        file_name=(prefix + "equipment_images/circuit_board_manufacturing/lpkf_s104_pcb_router.jpg")
    )
    machine2.categories.append(circuit_board_manufacturing)
    session.add(machine2)
    session.commit()

    # Pick and Place
    machine3 = class_models.Machine(
        "Pick and Place",
        "https://psu-epl.github.io/doc/equip/misc/pickAndPlace/",
        file_name=(prefix + "equipment_images/circuit_board_manufacturing/pick_and_place.jpg")
    )
    machine3.categories.append(circuit_board_manufacturing)
    session.add(machine3)
    session.commit()

    # Soldering Equipment
    machine4 = class_models.Machine(
        "Soldering Equipment",
        "https://psu-epl.github.io/doc/equip/solder/Soldering-Equipment",
        file_name=(prefix + "equipment_images/circuit_board_manufacturing/soldering_equipment.jpg")
    )
    machine4.categories.append(circuit_board_manufacturing)
    session.add(machine4)
    session.commit()

    # T200N Desktop Solder Oven
    machine5 = class_models.Machine(
        "T200N Desktop Solder Oven",
        "https://psu-epl.github.io/doc/equip/solder/oven/",
        file_name=(prefix + "equipment_images/circuit_board_manufacturing/t200n_desktop_solder_oven.jpg")
    )
    machine5.categories.append(circuit_board_manufacturing)
    session.add(machine5)
    session.commit()

    # Test and Measurement
    machine6 = class_models.Machine(
        "Test and Measurement",
        "https://psu-epl.github.io/doc/equip/testing/",
        file_name=(prefix + "equipment_images/circuit_board_manufacturing/test_and_measurement.jpg")
    )
    machine6.categories.append(circuit_board_manufacturing)
    session.add(machine6)
    session.commit()

    # 3D Printers
    three_d_printers = class_models.MachineTag("3D Printers")

    # Form 3 SLA Printer
    machine7 = class_models.Machine(
        "Form 3 SLA Printer",
        "https://psu-epl.github.io/doc/equip/printer/form2/",
        file_name=(prefix + "equipment_images/3d_printers/form_3_sla_printer.jpg")
    )
    machine7.categories.append(three_d_printers)
    session.add(machine7)
    session.commit()
    # Ultimaker3 Extended 3D Printer
    machine8 = class_models.Machine(
        "Ultimaker3 Extended 3D Printer",
        "https://psu-epl.github.io/doc/equip/printer/UM3/",
        file_name=(prefix + "equipment_images/3d_printers/ultimaker3_extended_3d_printer.jpg")
    )
    machine8.categories.append(three_d_printers)
    session.add(machine8)
    session.commit()

    # Machining Equipment
    machining_equipment = class_models.MachineTag("Machining Equipment")

    # Drill Press
    machine9 = class_models.Machine(
        "Drill Press",
        "https://psu-epl.github.io/doc/equip/machining/drillPress/",
        file_name=(prefix + "equipment_images/machining_equipment/drill_press.jpg")
    )
    machine9.categories.append(machining_equipment)
    session.add(machine9)
    session.commit()
    # Little Machine Shop Lathe
    machine10 = class_models.Machine(
        "Little Machine Shop Lathe",
        "https://psu-epl.github.io/doc/equip/machining/lathe/",
        file_name=(prefix + "equipment_images/machining_equipment/little_machine_shop_lathe.jpg")
    )
    machine10.categories.append(machining_equipment)
    session.add(machine10)
    session.commit()
    # Little Machine Shop Mill
    machine11 = class_models.Machine(
        "Little Machine Shop Mill",
        "https://psu-epl.github.io/doc/equip/machining/mill/",
        file_name=(prefix + "equipment_images/machining_equipment/little_machine_shop_mill.jpg")
    )
    machine11.categories.append(machining_equipment)
    session.add(machine11)
    session.commit()
    # WAZER
    machine12 = class_models.Machine(
        "WAZER",
        "https://psu-epl.github.io/doc/equip/machining/wazer/",
        file_name=(prefix + "equipment_images/machining_equipment/wazer.jpg")
    )
    machine12.categories.append(machining_equipment)
    session.add(machine12)
    session.commit()

    # Laser Cutters
    laser_cutters = class_models.MachineTag("Laser Cutters")

    # QD-1390 Laser Cutter
    machine13 = class_models.Machine(
        "QD-1390 Laser Cutter",
        "https://psu-epl.github.io/doc/equip/laser/QD-1390/",
        file_name=(prefix + "equipment_images/laser_cutters/qd-1390_laser_cutter.jpg")
    )
    machine13.categories.append(laser_cutters)
    session.add(machine13)

    session.commit()

    # Miscellaneous
    miscellaneous = class_models.MachineTag("Miscellaneous")

    # EZFORM SV 1217
    machine14 = class_models.Machine(
        "EZFORM SV 1217",
        "https://psu-epl.github.io/doc/equip/misc/EZFORM_SV_1217/",
        file_name=(prefix + "equipment_images/miscellaneous/ezform_sv_1217.jpg")
    )
    machine14.categories.append(miscellaneous)
    session.add(machine14)
    session.commit()
    # Silhouette Cameo
    machine15 = class_models.Machine(
        "Silhouette Cameo",
        "https://psu-epl.github.io/doc/equip/misc/cameo/",
        file_name=(prefix + "equipment_images/miscellaneous/silhouette_cameo.jpg")
    )
    machine15.categories.append(miscellaneous)
    session.add(machine15)
    session.commit()
    # Thermocut 115/E
    machine16 = class_models.Machine(
        "Thermocut 115/E",
        "https://psu-epl.github.io/doc/equip/misc/Thermocut/",
        file_name=(prefix + "equipment_images/miscellaneous/thermocut_115e.jpg")
    )
    machine16.categories.append(miscellaneous)
    session.add(machine16)
    session.commit()

    # Example training logs
    log1 = class_models.TrainingLog(user=student1, machine=machine1, trained_at=datetime.now() - timedelta(days=2))
    log2 = class_models.TrainingLog(user=student1, machine=machine14, trained_at=datetime.now() - timedelta(days=1))
    log3 = class_models.TrainingLog(user=student2, machine=machine5, trained_at=datetime.now() - timedelta(days=1))
    session.add_all([log1, log2, log3])
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
