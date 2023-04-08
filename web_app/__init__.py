from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Additions for integrating Google doc with app.
# See documentation here: https://developers.google.com/docs/api/quickstart/python

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy()

migrate = Migrate(app, db)
db.init_app(app)
