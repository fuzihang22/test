from .. import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
from hashlib import md5
from flask_login import UserMixin
from flask import session, request

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64))
    username = db.Column(db.String(64), index=True, unique=True)
    phone_number = db.Column(db.String(64))
    address = db.Column(db.String(64))
    buisness_name = db.Column(db.String(64))
    type_of_buisness = db.Column(db.String(64))
    abn = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    current_listings = db.relationship('Listing', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User: {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    address_for_pickup = db.Column(db.String) 
    abn = db.Column(db.String)
    food_products = db.relationship('IndividualProduct', backref='listing', lazy='dynamic')

class IndividualProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'))
    quantity = db.Column(db.Float)
    description = db.Column(db.String(64))
    category = db.Column(db.String(64))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))