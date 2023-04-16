from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import serial



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy()

migrate = Migrate(app, db)
db.init_app(app)

# Function for reading from serial port
def serial_data():
    PORT = "/dev/ttyUSB0" # Hardcoded for now - needs to be fixed - menu?
    BAUD = 9600
    while True: # Read in continuous loop
        try:
            ser = serial.Serial(port=PORT, baudrate=BAUD)
        except Exception as e:
            print("Error opening port: " + str(e))
            continue
        
        while True: 
            try:
                data = ser.readline().decode().strip()
                clean = data[2:] # Remove add'l chars '\x'
                clean_int = int(clean, 16) # Convert to base 16 int
                card_number = (clean_int >> 1)  & 0x7FFFF # Bitshift to remove parity and mask to isolate 19 bits
                facility_code = (clean_int >> 20)  & 0xFFFF # Same for facility code
                print(card_number) # Verified when tested with my badge
                print(facility_code) # Not verified - No idea what my facility code should be
                
            except Exception as e:
                print(f"Error reading data from serial port: {str(e)}")
                continue

serial_data() # Call the above function when the app starts