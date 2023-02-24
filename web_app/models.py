from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String)

    def __repr__(self):
        return f"({self.id} {self.firstname} {self.lastname})"
    
# Manager class
# Inherits from User class
# Adds Boolean value for can_edit - flag indicates this user has permission to edit User records.

class Manager(User):
    can_edit = db.Column(db.Boolean)
    def __init__(self, id, fname, lname, email):
        super().init(self, id, fname, lname, email)
        self.can_edit = True

    def __repr__(self):
        return f"({self.id} {self.firstname} {self.lastname})"

# Admin class
# Inherits from Manager class
# Adds Boolean value for can_add and can_delete
  
class Admin(Manager):
    can_add = db.Column(db.Boolean)
    can_delete = db.Column(db.Boolean)
    
    def __init__(self, id, fname, lname, email):
        super().init(self, id, fname, lname, email)
        self.can_add = True
        self.can_delete = True   
    
    def __repr__(self):
        return f"({self.id} {self.firstname} {self.lastname})"
