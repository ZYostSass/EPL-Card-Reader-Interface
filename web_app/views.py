from flask import Flask, render_template, request, redirect, escape
from .models import User
from . import db
from . import app




@app.route("/")
def index():
    return render_template('index.html')

# Pulling from the database


@app.route('/read-user/', defaults={'id': 1})
@app.route("/read-user/<id>")
def test_read(id):
    user = db.get_or_404(User, id)
    return render_template('read_user.html', user=user)


# Inserting into the database
@app.route("/add-user/<name>")
def test_write(name):
    user = User(
        firstname=name,
    )
    db.session.add(user)
    db.session.commit()

    return render_template('added_user.html', user=user)

# Adding new user into database from form
# TODO: Only allow access to this page when logged in as an Admin or Manager


@app.route("/add-user-form/", methods=['POST', 'GET'])
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
            firstname=user_fname,
            lastname=user_lname,
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


@ app.route("/dashboard/")
def dashboard():
    return render_template("dashboard.html")


@ app.route("/equipOverview/")
def equipOverview():
    return render_template("equipOverview.html")


@ app.route("/equipOverview/student/")
def equipStudent():
    return render_template("equipStudent.html")


@ app.route("/permissions/")
def permissions():
    return render_template("permissions.html")


@ app.route("/waiver/")
def waiver():
    return render_template('waiver.html')


@app.route("/account_creation_form/")
def account_creation_form():
    return render_template("account_creation_form.html")