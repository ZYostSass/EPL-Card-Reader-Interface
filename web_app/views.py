from flask import Flask, render_template
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
        firstname = name,
    )
    db.session.add(user)
    db.session.commit()
    
    return render_template('added_user.html', user=user)

@app.route("/dashboard/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/equipOverview/")
def equipOverview():
    return render_template("equipOverview.html")


@app.route("/equipOverview/student/")
def equipStudent():
    return render_template("equipStudent.html")


@app.route("/permissions/")
def permissions():
    return render_template("permissions.html")


@app.route("/waiver/")
def waiver():
    return render_template("waiver.html")
