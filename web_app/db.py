from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_seeder import FlaskSeeder

db = SQLAlchemy()
migrate = Migrate()
seeder = FlaskSeeder()

def init_db(app):
    db.init_app(app)
    migrate.init_app(app, db)
    seeder.init_app(app, db)
