from flask import Flask, render_template, request, redirect, escape, Blueprint, session
from .models import User
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


@bp.route("/add-user-form/", methods=['POST', 'GET'])
def add_user_form():

    if request.method == "POST":
        user_id = request.form['id']
        user_fname = request.form['fname']
        user_lname = request.form['lname']
        user_email = request.form['email']

        # Check for all form fields
        if not user_id or not user_fname or not user_lname or not user_email:
            error_statement = "All form fields are required"
            return render_template("add_user_form.html",
                                   error_statement=error_statement,
                                   id=user_id,
                                   firstname=user_fname,
                                   lastname=user_lname,
                                   email=user_email)

        new_user = User(
            id=user_id,
            fname=user_fname,
            lname=user_lname,
            email=user_email
        )

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

@bp.route("/permissions/student/")
def permissionsStudent():
    return render_template("permissionsStudent.html")
