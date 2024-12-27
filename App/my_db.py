from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import and_

db = SQLAlchemy()

# users table
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    client_id = db.Column(db.String(255), unique=True)
    token = db.Column(db.String(255))
    login = db.Column(db.Integer)
    read_access = db.Column(db.Integer)     
    write_access = db.Column(db.Integer)   
    email = db.Column(db.String(30))

    
    def __init__(self, name, client_id, token, login, read_access, write_access, email):
        self.name = name
        self.client_id = client_id
        self.token = token
        self.login = login
        self.read_access = read_access
        self.write_access = write_access
        self.email = email

# Get a user with their client_id
def get_user_row_if_exists(client_id):
    return User.query.filter_by(client_id=client_id).first()

# Add a user to User table
def add_user_and_login(name, client_id, email, token=None):
    user = get_user_row_if_exists(client_id)
    
    if user:
        user.login = 1
        if token:
            user.token = token
        db.session.commit()
    else:
        new_user = User(name, client_id, token, 1, 0, 0, email)
        db.session.add(new_user)
        db.session.commit()

# Get all users
def get_all_users():
    return User.query.all()

# Update user access levels
def update_user_access(user_id, read_access=None, write_access=None):
    user = User.query.get(user_id)
    if user:
        if read_access is not None:
            user.read_access = read_access
        if write_access is not None:
            user.write_access = write_access
        db.session.commit()
        return True
    return False

# Get user_id from their client id
def get_user_id(client_id):
    user = User.query.filter_by(client_id=client_id).first()
    return user.id if user else None

class Parking_Lot(db.Model):
    __tablename__ = "parking_lot"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parking_spot = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __init__(self, user_id, parking_spot, status):
        self.user_id = user_id
        self.parking_spot = parking_spot
        self.status = status

# Add an entry for a parking_space status for the parking lot ( belonging to specific user )
def add_parking_status(user_id, parking_spot, status):
    user = User.query.get(user_id)
    if user:
        new_parking_entry = Parking_Lot(user_id=user_id, parking_spot=parking_spot, status=status)
        db.session.add(new_parking_entry)
        db.session.commit()
        return new_parking_entry
    else:
        raise ValueError("User with the given ID does not exist.") 

# Get all the the entries in the parking_lot table for logged in user
def get_parking_entries_by_user(user_id):
    return Parking_Lot.query.filter_by(user_id=user_id).all()