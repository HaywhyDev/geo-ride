from . import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    password_hash:str|int = db.Column(db.String(128), nullable=False)
    role:str = db.Column(db.String(50), nullable=False)
    license_number:str = db.Column(db.String(50), nullable=True)  
    balance:str = db.Column(db.String(50), default="0.0")
    phone_number = db.Column(db.String(20))
    
    
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pickup_location = db.Column(db.String(255), nullable=False)
    destination = db.Column(db.String(255), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='new')  # 'new', 'completed', etc.

    user = db.relationship('User', foreign_keys=[user_id])
    driver = db.relationship('User', foreign_keys=[driver_id])