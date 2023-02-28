from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String)
    can_edit = db.Column(db.Boolean)
    can_add = db.Column(db.Boolean)
    can_delete = db.Column(db.Boolean)
    
    def __init__(self, id, fname, lname, email):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.email = email
        self.can_edit = False
        self.can_add = False
        self.can_delete = False
        
    def __repr__(self):
        return f"({self.id} {self.firstname} {self.lastname})"
    
# Manager class
# Inherits from User class
# Adds Boolean value for can_edit - flag indicates this user has permission to edit User records.

class Manager(User):
    
    def __init__(self, id, fname, lname, email):
        super().init(self, id, fname, lname, email)
        self.can_edit = True
        self.can_add = False
        self.can_delete = False
        
    def __repr__(self):
        return f"({self.id} {self.firstname} {self.lastname})"

# Admin class
# Inherits from Manager class
# Adds Boolean value for can_add and can_delete
  
class Admin(Manager):
     
    def __init__(self, id, fname, lname, email):
        super().init(self, id, fname, lname, email)
        self.can_edit = True
        self.can_add = True
        self.can_delete = True   
    
    def __repr__(self):
        return f"({self.id} {self.firstname} {self.lastname})"
    
    
    def promoteManager(lucky_user):
        new_mgr = Manager(id=lucky_user.id,firstname=lucky_user.firstname,lastname=lucky_user.lastname,email=lucky_user.lastname)
        db.session.delete(lucky_user)
        db.session.add(new_mgr)
        db.session.commit()
        return new_mgr
    
    def promoteAdmin(lucky_mgr):
        new_admin = Manager(id=lucky_mgr.id,firstname=lucky_mgr.firstname,lastname=lucky_mgr.lastname,email=lucky_mgr.email)
        db.session.delete(lucky_mgr)
        db.session.add(new_admin)
        db.session.commit()
        return new_admin
