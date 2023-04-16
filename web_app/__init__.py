from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import serial



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy()

migrate = Migrate(app, db)
db.init_app(app)

def serial_data():
    print("Reading data...")
    PORT = "/dev/ttyUSB0"
    BAUD = 9600
    BYTESIZE = serial.EIGHTBITS
    TIMEOUT = 0
    while True:
        try:
            ser = serial.Serial(port=PORT, baudrate=BAUD)
        except Exception as e:
            print("Error opening port: " + str(e))
            continue
        
        while True: 
            try:
                data = ser.readline().decode().strip()
                clean = data[2:]
                clean_int = int(clean, 16)
                print(clean_int)
                card_number = (clean_int >> 1)  & 0x7FFFF # Bitshift to remove parity and mask to isolate 19 bits
                facility_code = (clean_int >> 20)  & 0xFFFF # Same for facility code
                print(card_number)
                print(facility_code)
                
            except Exception as e:
                print(f"Error reading data from serial port: {str(e)}")
                continue

serial_data()