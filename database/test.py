#import database_init
import user_options

#from flask import Flask
#app = Flask(__name__)
#@app.route("/")
#def hello_world():
#    return "<p>Hellow, World!</p>"

#user_options.checkin_user(0)
user_options.read_all()
# Duplicate user check
user_options.add_new_user(0, "John", "Doe", "jdoe@pdx.edu", "Admin")
# New User Addition
user_options.add_new_user(1, "Jane", "Jackson", "jjack@pdx.edu", "Student")
#user_options.user_check("John", "Doe")
#user_options.change_user_training(1,1,1)
# user_options.chance_user_access_level()
#user_options.change_user_access_level(1, "Manager")
user_options.read_all()
