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