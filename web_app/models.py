from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String)
    can_edit = db.Column(db.Boolean)
    can_add = db.Column(db.Boolean)
    can_delete = db.Column(db.Boolean)
    is_active = db.Column(db.Boolean)
    
    def __init__(self, id, fname, lname, email, active):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.email = email
        self.is_active = active
        self.can_edit = False
        self.can_add = False
        self.can_delete = False
        self.is_authenticated = False  
        
        
    def __repr__(self):
        return f"({self.id} {self.firstname} {self.lastname})"
    
    # These functions have been added to the model to meet requirements for flask-login (https://flask-login.readthedocs.io/en/latest/)
    # Logic will be implemented as I read through the docs.
    
    # is_authenticated(self):
    # "This property should return True if the user is authenticated, i.e. they have provided valid credentials. 
    # (Only authenticated users will fulfill the criteria of login_required.)" - from docs
    # For now, this returns the property is_authenticated, set to False initially.
 
    def is_authenticated(self):
      return self.is_authenticated
    
    # is_active(self):
    # "This property should return True if this is an active user - 
    # in addition to being authenticated, they also have activated their account, 
    # not been suspended, or any condition your application has for rejecting an account. 
    # Inactive accounts may not log in (without being forced of course).# -from docs
    # Returns this fiels 

    def is_active(self):
      return self.is_active
    
    # is_anonymous(self):
    # "This property should return True if this is an anonymous user. (Actual users should return False instead.)" - from docs.
    # Since I don't foresee this system having anonymous users, this function simply returns False.
    
    def is_anonymous(self):
      return False
    
    # get_id(self):
    # "This method must return a str that uniquely identifies this user, and can be used to load the user from the user_loader callback. 
    #  Note that this must be a str - if the ID is natively an int or some other type, you will need to convert it to str." - from docs.
    # This method returns the psu id number converted to a string.
    
    def get_id(self):
      return str(self.id)
    
    
# Manager class
# Inherits from User class
# Adds Boolean value for can_edit - flag indicates this user has permission to edit User records.

class Manager(User):
    
    def __init__(self, id, fname, lname, email, active):
        super().init(self, id, fname, lname, email, active)
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
        new_mgr = Manager(id=lucky_user.id,firstname=lucky_user.firstname,lastname=lucky_user.lastname,email=lucky_user.lastname, active=True)
        db.session.delete(lucky_user)
        db.session.add(new_mgr)
        db.session.commit()
        return new_mgr
    
    def promoteAdmin(lucky_mgr):
        new_admin = Manager(id=lucky_mgr.id,firstname=lucky_mgr.firstname,lastname=lucky_mgr.lastname,email=lucky_mgr.email, active=True)
        db.session.delete(lucky_mgr)
        db.session.add(new_admin)
        db.session.commit()
        return new_admin
