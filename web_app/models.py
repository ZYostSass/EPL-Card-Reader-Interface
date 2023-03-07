from flask import g

from .db import db

class User(db.Model): # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String)
    badge = db.Column(db.String)
    manager = db.Column(db.Boolean)
    admin = db.Column(db.Boolean)

    def __init__(self, id, fname, lname, email, badge, manager, admin):
        self.id = id
        self.firstname = fname
        self.lastname = lname
        self.email = email
        self.badge = badge
        self.manager = manager
        self.admin = admin

    @staticmethod
    def admin(id, fname, lname, email, badge):
        return User(id, fname, lname, email, badge, True, True)

    @staticmethod
    def manager(id, fname, lname, email, badge):
        return User(id, fname, lname, email, badge, True, False)

    def __repr__(self):
        return f"({self.id} {self.firstname} {self.lastname})"
