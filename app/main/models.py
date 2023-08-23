from .. import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
from hashlib import md5
from flask_login import UserMixin
from flask import session, request
import requests
import json
'''
BIG TODO: Segment into a donor and receiver models
In an ideal scenario, we would distinguish between the two types of users, and only save the required information.
For the current moment they are just built into the user model for testing purposes

current_listings - Db relationship to each listing created by this user.
accepted_listings - Db relationship to each listing accepted by this user
'''
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
    current_listings = db.relationship('Listing', backref='author', lazy='dynamic', foreign_keys='Listing.user_id')
    accepted_listings = db.relationship('Listing', backref='accepteduser', lazy='dynamic', foreign_keys='Listing.accepted_user_id')

    def __repr__(self):
        return '<User: {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

'''
Holds related info for each listing

food_products - Db relationship to each individual product for this listing.

listing.author - Returns the user that created the listing
listing.accepteduser - returns the user that accepted the listing
'''
class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    address = db.Column(db.String) 
    abn = db.Column(db.String)
    food_products = db.relationship('IndividualProduct', backref='listing', lazy='dynamic')
    accepted_listing = db.Column(db.Boolean, default=False, nullable=False)
    accepted_user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    def setMapCoords(self):
        URL = "https://geocode.maps.co/search?q=" + self.author.address
        #TODO Higher validation of address once address is properly set up in the db
        r = requests.get(url = URL)
        data = r.json()
        try:
            latitude = data[0]['lat']
            longitude = data[0]['lon']
        except:
            latitude = 0.0
            longitude = 0.0
        self.latitude = latitude
        self.longitude = longitude

'''
Holds the quantity, description and category for each indivdual item that a Donor wants to sell

IndividualProduct.listing - returns the listing that this product belongs to
'''
class IndividualProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'))
    quantity = db.Column(db.Float)
    description = db.Column(db.String(64))
    category = db.Column(db.String(64))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))