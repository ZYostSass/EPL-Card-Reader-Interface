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

q = queue.Queue()
ser = CardReader(port='/dev/ttyUSB0', baud_rate=9600)


def read_serial(q):
    while True:
        card_number, facility_code = ser.read_serial()
        if card_number and facility_code:
            q.put((card_number, facility_code))


thread = Thread(target=read_serial, args=(q,))
thread.daemon = True
thread.start()

