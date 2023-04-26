from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from card_reader.reader import CardReader
from threading import Thread
import queue


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy()

migrate = Migrate(app, db)
db.init_app(app)

# Callback function for reader thread
# Still doesn't execute correctly
# Input is correctly interpreted in test.py
def card_input(data):
    print(f"Data received: {data}")
    clean = data[2:]
    print(f"Clean: {clean}")
    clean_int = int(clean, 16)
    card_number = (clean_int >> 1)  & 0x7FFFF # Bitshift to remove parity and mask to isolate 19 bits
    facility_code = (clean_int >> 20)  & 0xFFFF # Same for facility code
    print(card_number) # Verified when tested with my badge
    print(facility_code) # Not verified - No idea what my facility code should be

q = queue.Queue()
ser = CardReader(port='/dev/ttyUSB0', baud_rate=9600, callback=card_input)


def read_serial(q):
    while True:
        card_number, facility_code = ser.read_serial()
        if card_number and facility_code:
            card_data = (card_number, facility_code)
            q.put(card_data)


thread = Thread(target=read_serial, args=(q,))
thread.daemon = True
thread.start()

