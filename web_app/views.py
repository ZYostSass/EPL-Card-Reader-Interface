from flask import Flask, render_template
from . import app


@app.route("/")
def index():
    return render_template('index.html')


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
