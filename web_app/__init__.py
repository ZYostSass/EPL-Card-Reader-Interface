from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from card_reader.reader import CardReader
from flask_seeder import FlaskSeeder
import os
import serial, serial.tools.list_ports


app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"


try:
  os.makedirs(app.instance_path)
except OSError:
  pass

db = SQLAlchemy()

port = None
try:
  port = serial.Serial('COM3', 9600, timeout=1)
except Exception as e:
  print(f"An error occurred: {e}") # Fails here too.  Does not fail

card_reader = CardReader(serial_port=port) 
migrate = Migrate()
seeder = FlaskSeeder()

db.init_app(app)
migrate.init_app(app, db)
seeder.init_app(app, db)

from .admin import bp as admin_bp

app.register_blueprint(admin_bp)

from .views import bp as views_bp

app.register_blueprint(views_bp)