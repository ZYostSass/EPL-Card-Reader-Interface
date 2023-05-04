from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from card_reader.reader import CardReader
from flask_seeder import FlaskSeeder
import os



app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# app.config["EXPLAIN_TEMPLATE_LOADING"] = True

try:
  os.makedirs(app.instance_path)
except OSError:
  pass

db = SQLAlchemy()

card_reader = CardReader() # Note- add option for timeout prefs?
migrate = Migrate()
seeder = FlaskSeeder()

db.init_app(app)
migrate.init_app(app, db)
seeder.init_app(app, db)

from .admin import bp as admin_bp

app.register_blueprint(admin_bp)

from .views import bp as views_bp

app.register_blueprint(views_bp)