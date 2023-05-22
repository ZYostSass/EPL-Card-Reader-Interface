from flask import Flask, g, session
from card_reader.reader import CardReader
import os

from database.user_options import get_user_by_id

app = Flask(__name__)
app.debug = True
app.config["SECRET_KEY"] = "dev"
app.config["EXPLAIN_TEMPLATE_LOADING"] = True

try:
  os.makedirs(app.instance_path)
except OSError:
  pass

# Commented out until card reader fix for other OS
card_reader = CardReader() # Note- add option for timeout prefs?

from .views import admin_bp

app.register_blueprint(admin_bp)

from .views import bp as views_bp

app.register_blueprint(views_bp)

@app.context_processor
def add_current_role():
    if g.user is not None:
       return dict(current_role=g.user.role)
    else: 
      return dict(current_role=None)
    
@app.before_request
def set_user_global():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        user = get_user_by_id(user_id)
        g.user = user
