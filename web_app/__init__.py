from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from card_reader.reader import CardReader
from flask_seeder import FlaskSeeder
import os
import multiprocessing
import subprocess
from flask.cli import ScriptInfo


app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"


try:
  os.makedirs(app.instance_path)
except OSError:
  pass

db = SQLAlchemy()


card_reader = CardReader() 
migrate = Migrate()
seeder = FlaskSeeder()

db.init_app(app)
migrate.init_app(app, db)
seeder.init_app(app, db)

from .admin import bp as admin_bp

app.register_blueprint(admin_bp)

from .views import bp as views_bp

app.register_blueprint(views_bp)

def start_card_reader():
    with app.app_context():
        card_reader.start_reading_loop()


card_reader_process = multiprocessing.Process(target=start_card_reader)
card_reader_process.start()

def start_card_reader():
  with app.app_context():
      card_reader.start_reading_loop()


if __name__ == "__main__":
  freeze_support()  # Add this line
  card_reader_process = multiprocessing.Process(target=start_card_reader)
  card_reader_process.start()

  app.run()