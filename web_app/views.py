from flask import Flask, render_template, request, redirect, escape, Blueprint, session, jsonify, make_response
from database.class_models import *
from database.user_options import add_new_user, remove_user
from .admin import login_required
from . import db, card_reader
from sqlalchemy.orm.exc import NoResultFound
import serial, serial.tools.list_ports


bp = Blueprint('views', __name__)

@bp.route("/")
def index():
    return render_template('index.html')

@bp.route("/login")
def login():
  if request.method == "POST":
      user_email = request.form['email']
      password = request.form['password']

      # Verify password
      user = db.session.get(User, id) #STUB< NEEDS TO BE REPLACED WITH A PASSWORD CHECK

      if user is None:
          return render_template("login.html", error="Failed to verify username or password") #STUB< Page needs to be implemented
      else:
          session["user_id"] = user.id
          redirect_arg = request.args.get('next')
          if redirect_arg is None:
              return redirect("/", code=302)
          else:
              return redirect(redirect_arg, code=302)


  return render_template("login.html")

  @bp.route("/logout")
  def login(id):
      session.pop('username', None)
      return redirect(url_for('index'))


# Pulling from the database


@bp.route('/read-user/', defaults={'id': 1})
@bp.route("/read-user/<id>")
def test_read(id):
    user = db.get_or_404(User, id)
    return render_template('read_user.html', user=user)


# Inserting into the database
@bp.route("/add-user/<name>")
@login_required
def test_write(name):
    user = User(
        firstname=name,
    )
    db.session.add(user)
    db.session.commit()

    return render_template('added_user.html', user=user)

# Adding new user into database from form
# TODO: Only allow access to this page when logged in as an Admin or Manager

#Zach: Set default role to always be student at this time.

@bp.route("/add-user-form/", methods=['POST', 'GET'])
def add_user_form():
    
    if request.method == "POST":
        user_id = request.form['id']
        user_badge = request.form['access']
        user_fname = request.form['fname']
        user_lname = request.form['lname']
        user_email = request.form['email']
     #   user_role = request.form['role']

        # Check for all form fields
        if not user_id or not user_badge or not user_fname or not user_lname or not user_email:
            error_statement = "All form fields are required"
            return render_template("add_user_form.html",
                                   error_statement=error_statement,
                                   id=user_id,
                                   badge = user_badge,
                                   firstname=user_fname,
                                   lastname=user_lname,
                                   email=user_email)
       #                            role = user_role)

        try:
            add_new_user(user_id, user_badge, user_fname, user_lname, user_email, "Admin")
            return redirect('/add-user-form/')
        except:
            # TODO: Add a fail html page to handle error outputs
            return f"(Error adding {user_fname} {user_lname} to the database)"

    else:
        return render_template("add_user_form.html")


@bp.route("/dashboard/")
def dashboard():
    return render_template("dashboard.html")


@bp.route("/equipOverview/")
def equipOverview():
    return render_template("equipOverview.html")


@bp.route("/equipOverview/student/")
def equipStudent():
    return render_template("equipStudent.html")


@bp.route("/permissions/")
def permissions():
    return render_template("permissions.html")


@bp.route("/waiver/")
def waiver():
    return render_template('waiver.html')



# Route for the card reader test page
@bp.route("/card_test/", methods=['GET'])
def card_test():
  return render_template('card_test.html')
# Route for checking the queue where card data gets read to
# Using flask.make_response and flask.jsonify to create an http response header.
# https://tedboy.github.io/flask/generated/flask.make_response.html
# https://tedboy.github.io/flask/generated/flask.jsonify.html
# https://api.jquery.com/ (Used in card_test.html to update page)

@bp.route("/card_data/")
def card_data():
    card_data = card_reader.get_data()
    print(card_data)
    if card_data is not None:
        card_number, facility_code = card_data
    else:
        card_number, facility_code = None, None

    return jsonify(card_number=card_number, facility_code=facility_code)

    
@bp.route("/permissions/student/")
def permissionsStudent():
    return render_template("permissionsStudent.html")

@bp.route("/account-creation-form/", methods=['POST', 'GET'])
def account_creation_form():
   #for some reason I'm not getting a post call on submit.  
   if request.method == "POST":
        user_id = request.form['id']
        user_fname = request.form['fname']
        user_lname = request.form['lname']
        user_email = request.form['email']
        #grab data from radio button for promote user automatically
        
        # Check for all form fields
        #method from user_options.py no intial reaction, but this may
        #be from some other error in the route. tbd...
        add_new_user(user_id, 0, user_fname, user_lname, user_email, "Admin")            
        return("User data: is" + user_id + user_fname)

   else: 
    return render_template("account_creation_form.html")


@bp.route("/edit_user/")
def edit_user():
    return render_template('edit_user.html')

@bp.route('/remove-user/', methods=['GET', 'POST'])
def remove_user_form():
    if request.method == "POST":
        user_id = request.form['id']
        try:
            remove_user(user_id)
            return redirect('/remove-user/')
        except:
            return f"(Error; not in database.)"
    else:
        return render_template("remove_user_form.html")

