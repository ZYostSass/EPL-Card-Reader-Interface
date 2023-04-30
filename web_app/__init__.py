from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from card_reader.reader import CardReader



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy()
card_reader = CardReader(port='/dev/ttyUSB0', baud_rate=9600) # Note- add option for timeout prefs?
migrate = Migrate(app, db)
db.init_app(app)



