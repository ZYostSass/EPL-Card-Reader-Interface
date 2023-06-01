import base64
import datetime
from flask_socketio import SocketIO
from flask import Flask, g, session
from card_reader.reader import CardReader
import os
from database.class_models import LOGOUT_TIME

from database.user_options import get_int_key, get_user_by_id
from datetime import datetime, timedelta

#TODO: Store this in a seperate database table
LOGOUT_TIME_DEFAULT = 30 # minutes

async_mode = None

app = Flask(__name__)
app.debug = True
app.config["SECRET_KEY"] = "dev"
app.config["EXPLAIN_TEMPLATE_LOADING"] = True
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 # 16 MB

socketio = SocketIO(app, async_mode=async_mode)


try:
  os.makedirs(app.instance_path)
except OSError:
  pass

card_reader = None # Note- add option for timeout prefs?

def get_card_reader():
  global card_reader
  if card_reader is None:
    card_reader = CardReader(fake=app.debug)

  return card_reader

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
        session.pop("user_id", None)
        session.pop("user_active_at", None)
        return  
    
    diff = datetime.now() - timedelta(minutes=log_out_time)
    diff = diff.replace(tzinfo = None)
    last_login_time = last_login_time.replace(tzinfo = None)

    if last_login_time < diff:
        session.pop("user_id", None)
        session.pop("user_active_at", None)
        g.user = None
    else:
        session["user_active_at"] = datetime.now()
        user = get_user_by_id(user_id)
        g.user = user

@app.template_filter('format_category')
def format_category(value):
    if value is not None:
      return value.replace("_", " ").title()
    return "NONE"

@app.template_filter('format_trained_at')
def format_trained_at(value):
    if value is not None and isinstance(value, datetime):
      data = value.strftime("%Y-%m-%d")
    else:
      data = "NONE"
    return data

# The following was written by chatgpt:
@app.template_filter('base64_to_data_url')
def base64_to_data_url(value):
    if value is not None:
      data = value.decode('utf-8')
    else:
      data = ""
    return f"data:image/jpg;base64,{data}"