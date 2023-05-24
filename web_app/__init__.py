import base64
import datetime
from flask import Flask, g, session
#from card_reader.reader import CardReader
import os

from database.user_options import get_user_by_id

app = Flask(__name__)
app.debug = True
app.config["SECRET_KEY"] = "dev"
app.config["EXPLAIN_TEMPLATE_LOADING"] = True
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 # 16 MB

try:
  os.makedirs(app.instance_path)
except OSError:
  pass

# Commented out until card reader fix for other OS
# card_reader = CardReader() # Note- add option for timeout prefs?

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

@app.template_filter('format_category')
def format_category(value):
    if value is not None:
      return value.replace("_", " ").title()
    return "NONE"

@app.template_filter('format_trained_at')
def format_trained_at(value):
    if value is not None and isinstance(value, datetime.datetime):
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