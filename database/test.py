#import database_init
import user_options

#from flask import Flask
#app = Flask(__name__)
#@app.route("/")
#def hello_world():
#    return "<p>Hellow, World!</p>"

# user_options.checkin_user()
#user_options.add_new_user(1,1,"student","a","a")
user_options.read_all()
#user_options.user_check("John", "Doe")
user_options.change_user_training(1,1,1)
# user_options.chance_user_access_level()
user_options.read_all()
