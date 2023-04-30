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
# TODO: Adjust this route once finalized schema is merged
@app.route("/add-user-form/", methods=['POST', 'GET'])
def add_user_form():

    if request.method == "POST":
        user_idnumber = request.form['idnumber']
        user_fname = request.form['fname']
        user_lname = request.form['lname']
        user_email = request.form['email']

        # Check for all form fields
        if not user_idnumber or not user_fname or not user_lname or not user_email:
            error_statement = "All form fields are required"
            return render_template("add_user_form.html",
                                   error_statement=error_statement,
                                   idnumber=user_idnumber,
                                   fname=user_fname,
                                   lname=user_lname,
                                   email=user_email)

        new_user = User(
            idnumber=user_idnumber,
            fname=user_fname,
            lname=user_lname,
            email=user_email,
            role="Student"
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            success_statement = "User added successfully"
            return redirect('/add-user-form/', success_statement=success_statement)
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
