from . import db

from flask import g

from .db import db

MANAGER = "manager"
ADMIN = "manager"
USER = "user"

class User(db.Model): # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String)
    badge = db.Column(db.String)
    role = db.Column(db.String)

    def __init__(self, id, fname, lname, email, badge, role):
        self.id = id
        self.firstname = fname
        self.lastname = lname
        self.email = email
        self.badge = badge
        self.role = role

    def user(self, id, fname, lname, email, badge, role):
      self.__init__(id, fname, lname, email, badge, USER)

    def manager(self, id, fname, lname, email, badge, role):
      self.__init__(id, fname, lname, email, badge, MANAGER)

    def admin(self, id, fname, lname, email, badge, role):
      self.__init__(id, fname, lname, email, badge, ADMIN)

    def is_admin(self):
      return self.role == ADMIN

    def is_manager(self):
      return self.role == MANAGER

    def is_user(self):
      return self.role == USER
