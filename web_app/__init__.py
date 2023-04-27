from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import queue
from threading import Thread
from card_reader.reader import CardReader


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy()

migrate = Migrate(app, db)
db.init_app(app)

q = queue.Queue()
# Callback function for reader thread
# Function is passed to CardReader constructor as callback
# When CardReader.read_serial() reads data, it passes to this function 
# Card data is parsed and dropped into Queue for access elsewhere.
# 
def card_input(data):
    print(f"Data received: {data}")
    clean = data[2:]
    print(f"Clean: {clean}")
    clean_int = int(clean, 16)
    card_number = (clean_int >> 1)  & 0x7FFFF # Bitshift to remove parity and mask to isolate 19 bits
    facility_code = (clean_int >> 20)  & 0xFFFF # Same for facility code
    print(card_number) # Verified when tested with my badge
    print(facility_code) # Not verified - No idea what my facility code should be
    card_data = (card_number, facility_code)
    q.put(card_data)
    print(f"Added card data to queue: {card_data}")
    print(f"Queue contents: {list(q.queue)}")


ser = CardReader(port='/dev/ttyUSB0', baud_rate=9600, callback=card_input)


def read_serial(q):
    print("Read called!")
    while True:
        try:
            print("Inside read loop")
            card_number, facility_code = ser.read_serial()
            if card_number and facility_code:
                card_data = (card_number, facility_code)
                q.put(card_data)
                print(f"Added card data to queue: {card_data}")
                print(f"Queue contents: {list(q.queue)}")
        except TimeoutError:
            print("Timed out!")
            pass
        except Exception as e:
            print(f"Error in read_serial loop:  {e}")


# Start the read_serial function in a new thread as a background process
thread = Thread(target=read_serial, args=(q,))
thread.daemon = True
thread.start()

