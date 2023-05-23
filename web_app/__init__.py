from flask import Flask, g, session
#from card_reader.reader import CardReader
import os
from database.class_models import LOGOUT_TIME

from database.user_options import get_int_key, get_user_by_id
from datetime import datetime, timedelta

#TODO: Store this in a seperate database table
LOGOUT_TIME_DEFAULT = 30 # minutes

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"
app.config["EXPLAIN_TEMPLATE_LOADING"] = True

try:
  os.makedirs(app.instance_path)
except OSError:
  pass

# Commented out until card reader fix for other OS
#card_reader = CardReader(baud_rate=9600) # Note- add option for timeout prefs?

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
    last_login_time = session.get("user_active_at")
    log_out_time = get_int_key(LOGOUT_TIME)

    if log_out_time is None:
       log_out_time = LOGOUT_TIME_DEFAULT
       
    if user_id is None or last_login_time is None:
        g.user = None
    elif last_login_time < (datetime.now() - timedelta(minutes=log_out_time)):
        session.pop("user_id", None)
        session.pop("user_active_at", None)
        g.user = None
    else:
        session["user_active_at"] = datetime.datetime.now()
        user = get_user_by_id(user_id)
        g.user = user
