from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String)

    def __repr__(self):
        return f"({self.id} {self.firstname} {self.lastname})"