#import database_init
import user_options

#from flask import Flask
#app = Flask(__name__)
#@app.route("/")
#def hello_world():
#    return "<p>Hellow, World!</p>"

# Check in base admin - sure hit
print("Checking is user with ID: 0 (Base Admin)")
user_options.checkin_user(0)
# Check in unregistered user - sure miss
print("Checking is user with ID: 2345 (Doesn't Exist)")
user_options.checkin_user(2345)
# Output list of all users in database
print("Outputting all users in the table")
user_options.read_all()
# Duplicate user check
print("Adding duplicate Base Admin: John Doe")
user_options.add_new_user(0, "John", "Doe", "jdoe@pdx.edu", "Admin")
# New User Addition
print("Adding new user: Jane Jackson")
user_options.add_new_user(1, "Jane", "Jackson", "jjack@pdx.edu", "Student")
user_options.read_all()
# Remove added user
print("Removing new user: Jane Jackson")
user_options.remove_user(1)
user_options.read_all()

#user_options.user_check("John", "Doe")
#user_options.change_user_training(1,1,1)
# user_options.chance_user_access_level()
#user_options.change_user_access_level(1, "Manager")
user_options.read_all()
