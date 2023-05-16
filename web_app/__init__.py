from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_seeder import FlaskSeeder
import os
from flask_socketio import SocketIO
from card_reader.reader_svc import CardReader
from multiprocessing import Process, Lock



app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"



try:
  os.makedirs(app.instance_path)
except OSError:
  pass

db = SQLAlchemy()
socketio = SocketIO(app)
card_reader = CardReader(app) 
card_reader.set_socketio(socketio)


migrate = Migrate()
seeder = FlaskSeeder()

db.init_app(app)
migrate.init_app(app, db)
seeder.init_app(app, db)

app.card_reader = card_reader

from .admin import bp as admin_bp

app.register_blueprint(admin_bp)

from .views import bp as views_bp

app.register_blueprint(views_bp)

if __name__ == "__main__":
    lock = Lock()

    card_reader = CardReader(app)
    card_reader.set_socketio(socketio)

    card_reader_process = Process(target=card_reader.run)
    card_reader_process.start()

    socketio.run(app)

    # Global variable for the CardReader object
card_reader = None

# This function is called when the Flask app starts
def init_app():
    global card_reader
    card_reader = CardReader(app)
    card_reader.set_socketio(socketio)

# This function is called when the Flask app stops
def destroy_app():
    global card_reader
    card_reader.close()

# This code is run when the Flask app starts
with app.app_context():
  def before_first_request():
      init_app()

# This code is run when the Flask app stops
@app.teardown_appcontext
def teardown_appcontext(exception):
    destroy_app()