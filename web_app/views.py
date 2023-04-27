from flask import Flask, render_template, request, redirect, escape, jsonify, make_response
from .models import User
from . import db
from . import app
from . import q
import queue




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

# Route for the card reader test page
@ app.route("/card_test/", methods=['GET'])
def card_test():
    return render_template('card_test.html') # My current idea is blocking loading this - more research needed.

# Route for checking the queue where card data gets read to
# Using flask.make_response and flask.jsonify to create an http response header.
# https://tedboy.github.io/flask/generated/flask.make_response.html
# https://tedboy.github.io/flask/generated/flask.jsonify.html
# https://api.jquery.com/ (Used in card_test.html to update page)
@ app.route("/card_data/", methods=['GET'])
def card_data():
    response_data = None
    try:
        card_data = q.get(block=False)
    except queue.Empty:
        response_data = {}
        pass
    else:
        print(f"Q: {list(q.queue)}")
        response_data = {'card_number': card_data[0], 'facility_code': card_data[1]}
        with q.mutex:
            q.queue.clear()
        print(f"Queue: {list(q.queue)}")
    return make_response(jsonify(response_data))