from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from card_reader.reader import CardReader
from threading import Thread


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy()

migrate = Migrate(app, db)
db.init_app(app)

ser = CardReader(port='/dev/ttyUSB0', baud_rate=9600)
def start_reader():
    ser.read_serial()


thread = Thread(target=start_reader)
thread.start()# Call the above function when the app starts