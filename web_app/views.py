from flask import Flask, render_template, request, redirect, escape, Blueprint, session
from database.class_models import *
from database.user_options import add_new_user
from .admin import login_required

from . import db

bp = Blueprint('views', __name__)

@bp.route("/")
def index():
    return render_template('index.html')

@bp.route("/login")
def login(id):
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
        if not user_id or not user_fname or not user_lname or not user_email:
            error_statement = "All form fields are required"
            return render_template("add_user_form.html",
                                   error_statement=error_statement,
                                   id=user_id,
                                   badge = user_badge,
                                   firstname=user_fname,
                                   lastname=user_lname,
                                   email=user_email)
       #                            role = user_role)

        new_user = User(
            id=user_id,
            access=user_badge,
            fname=user_fname,
            lname=user_lname,
            email=user_email)
       #     role=user_role)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/add-user-form/')
        except:
            # TODO: Add a fail html page to handle error outputs
            return f"(Error adding {new_user.firstname} {new_user.lastname} to the database)"

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

@bp.route("/remove_user/")
def remove_user():
    return render_template('remove_user.html')
