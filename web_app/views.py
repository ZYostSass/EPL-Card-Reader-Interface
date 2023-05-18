from flask import Flask, render_template, request, redirect, escape, Blueprint, session, jsonify, make_response, flash, url_for
from database.class_models import *
from database.user_options import add_new_user, remove_user, read_all_machines, edit_machine, add_machine, remove_machine, change_user_access_level, check_user_password
from .admin import login_required
from . import db
from sqlalchemy.orm.exc import NoResultFound
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
# from wtforms.validators import DataRequired

bp = Blueprint('views', __name__)
# bp.config['SECRET_KEY'] = "asdfghjkl"

@bp.route("/")
def index():
    return render_template('index.html')

@bp.route("/login", methods=['POST', 'GET'])
def login():
  if request.method == "POST":
      user_email = request.form['email']
      password = request.form['password']

      # Verify password
      user = check_user_password(user_email, password) 

      if user is None:
          flash("Failed to verify username or password", "error")
          return render_template("login.html")
      else:
          session["user_id"] = user.id
          redirect_arg = request.args.get('next')
          if redirect_arg is None:
              return redirect("/", code=302)
          else:
              return redirect(redirect_arg, code=302)


  return render_template("login.html")

@bp.route("/logout")
def logout(id):
    session.pop('username', None)
    return redirect(url_for('index'))

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
        # TODO (if time): Function call to get badge number by scanning in
        # Otherwise, proceed with getting inputs via manual entry
        user_id = request.form['id']
        user_badge = request.form['badge']
        user_fname = request.form['fname']
        user_lname = request.form['lname']
        user_email = request.form['email']
        try:
            #Potential TODO: Change role from Admin to Student for this form (not sure why it's Admin currently)
            add_new_user(user_id, user_badge, user_fname, user_lname, user_email, "Admin")
            flash("User Added Successfully", "success")
            return redirect(url_for('views.add_user_form'))
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for('views.add_user_form'))

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
#@bp.route("/card_test/", methods=['GET'])
#def card_test():
#  return render_template('card_test.html')
# Route for checking the queue where card data gets read to
# Using flask.make_response and flask.jsonify to create an http response header.
# https://tedboy.github.io/flask/generated/flask.make_response.html
# https://tedboy.github.io/flask/generated/flask.jsonify.html
# https://api.jquery.com/ (Used in card_test.html to update page)

# @bp.route("/card_data/")
# def card_data():
#     card_data = card_reader.get_data()
#     if card_data is not None:
#         card_number, facility_code = card_data
#     else:
#         card_number, facility_code = None, None

#     return jsonify(card_number=card_number, facility_code=facility_code)

    
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
            flash("User Removed Successfully", "success")
            return redirect(url_for('views.remove_user_form'))
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for('views.remove_user_form'))
    else:
        return render_template("remove_user_form.html")

#Creating a form for promoting a user
class PromoteForm(FlaskForm):
    id = StringField("Enter PSU ID", [validators.DataRequired()])
    role = StringField("Update role", [validators.DataRequired()])
    submit = SubmitField("Update")

#Create a Promote Page
@bp.route("/promote", methods = ["POST", "GET"])
def PromoteUser():
    id = None
    role = None
    form = PromoteForm()
    #Validate Form
    if form.validate_on_submit():
        id = form.id.data
        role = form.role.data
        set_roles = ["student", "admin", "manager"]
        if (role):
            change_user_access_level(id, role)
            flash("Successfully updated")
            return redirect('/promote')    
        
    return render_template("promote_user.html",id = id, role= role, form = form)
    
@bp.route("/promote-dummy", methods =["GET","POST"])
def add_promote_dummy_data():
    for x in range(3):
        add_new_user(x +1,x,"A", "Nguyen", "123@pdx.edu", "student")
        # user = User(
        #     id = x,
        #     bagde= 1234,
        #     role = 'student',
        #     fname= 'A',
        #     lname= "Nguyen",
        #     email = '123@pdx.edu', 
        # )
        # db.session.add(user)
        # db.session.commit()
        
    return render_template("dashboard.html")
    
@bp.route('/manage-equipment/')
def manage_equipment():
    all_machine_data = read_all_machines()
    return render_template("manage_equipment.html", machines=all_machine_data)

@bp.route('/update-equipment/', methods = ['GET', 'POST'])
def update_equipment():
    if request.method == "POST":
        equipment_name = request.form.get("equipment_name")
        new_equipment_name = request.form.get("new_equipment_name")

        try:
            edit_machine(equipment_name, new_equipment_name)
            flash("Equipment Updated Successfully", "success")
        except ValueError as e:
            flash(str(e), "error")        

        return redirect(url_for('views.manage_equipment'))

@bp.route('/insert-equipment/', methods= ['POST'])
def insert_equipment():
    if request.method == 'POST':
        equipment_name = request.form['equipment_name']

        try:
            add_machine(equipment_name)
            flash("Equipment Added Successfully", "success")
        except ValueError as e:
            flash(str(e), "error")

        return redirect(url_for('views.manage_equipment'))
    
@bp.route('/remove-equipment/<name>', methods = ['GET', 'POST'])
def remove_equipment(name):
    try:
        remove_machine(name)
        flash("Equipment Removed Successfully", "success")
    except ValueError as e:
        flash(str(e), "error")

    return redirect(url_for('views.manage_equipment'))
