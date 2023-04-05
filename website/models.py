from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash

class Note(db.Model):
    # Database entry template for a note
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))   # Column contains data from the class User (foreign relationship)
    


class User(db.Model, UserMixin):
    # Database entry template for a user account
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())
    notes = db.relationship('Note') # Every time the user creates a new note, add its ID to the user's list

    def reset_password(self, new_password):
        self.password = generate_password_hash(new_password)