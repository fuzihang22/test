from flask import Flask, session, request, render_template, url_for, flash, redirect
from .. import login, db
from . import main
from .forms import LoginForm, SignUpForm, CreateListingForm, EditProfileForm, ChangePasswordForm, CreateListingEntryForm, AcceptListingForm, AccessListingForm
from markupsafe import escape
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from sqlalchemy.sql import func
from .models import User, Listing, IndividualProduct
import json

@main.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = func.now()
        db.session.commit()

'''
Handling login for users
session['name'] - On login stores the username, this can be called to find the username of the client
'''
@main.route("/", methods=['GET', 'POST'])
@main.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()  
    if request.method == 'POST':
        if current_user.is_authenticated:
            return redirect(url_for('main.home')) 
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('main.login'))
            session['name'] = form.username.data
            login_user(user, remember=form.rem_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.home')

        return redirect(next_page)
    else:
        return render_template("Login.html", form=form)

'''
Empty home page
TODO Fill with related information
'''
@main.route("/home")
@login_required
def home():
    user = User.query.filter_by(username=session['name']).first()
    return render_template("Home.html", title="HOME")

#Hangle logout routing
@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

'''
Handling signup page
TODO: Strong validation and error checking for values such as: phone number, address, email (maybe send registration email), abn
POST: Redirects to login page
GET: Displays signup form
'''
@main.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST':
        if current_user.is_authenticated:
            return redirect(url_for('main.home'))
        if form.validate_on_submit():
            user = User(username=form.username.data)
            user.set_password(form.password.data)
            user.email = form.email.data
            user.phone_number = form.phone_number.data
            user.address = form.address.data
            user.buisness_name = form.buisness_name.data
            user.type_of_buisness = form.type_of_buisness.data
            user.abn = form.abn.data
            db.session.add(user)
            db.session.commit()
            flash("Congratulations, you have signed up successfully!")
            return redirect(url_for('main.login'))
        return render_template('SignUp.html', title='Sign Up', form=form)
    else:
        return render_template('SignUp.html', title='Sign Up', form=form)

'''
Handling the creation of listings
GET: display create listing form
POST: Assign values to listing models. Constructs relationship between listing and each individual product
'''
@main.route("/createlisting", methods=['GET', 'POST'])
@login_required
def createlisting():
    form = CreateListingForm()
    user = User.query.filter_by(username=session['name']).first()
    if request.method == "POST":
        if form.validate_on_submit(): 
            listing = Listing(author=user)
            listing.address = user.address
            listing.abn = user.abn
            listing.setMapCoords()
            for product in form.product_list.data:
                indivdual_product = IndividualProduct(listing=listing)
                indivdual_product.quantity = product['quantity']
                indivdual_product.description = product['description']
                indivdual_product.category = product['category']

                db.session.add(indivdual_product)
                db.session.commit()
                
            return redirect(url_for('main.map'))
        return render_template('CreateListing.html', form=form, title="CREATE LISTING")
    return render_template('CreateListing.html', form=form, title="CREATE LISTING")

'''
Profile page
GET: Grabs user info to be displayed
'''
@main.route("/profile", methods=['GET'])
@login_required
def profile():
    user = User.query.filter_by(username=session['name']).first()
    listing = Listing.query.filter_by(author=user).all()
    return render_template('Profile.html', title="Profile", user_info=user, Listing=listing)

'''
Edit profile page
GET: Dynamically fills form with the current user values. 
POST: Reassigns each aspect of the user model (except password and listings) to the values of the form. Strong validation required. Maybe more elegant solution?idk 
'''
@main.route("/editprofile", methods=['GET', 'POST'])
@login_required
def editprofile():
    form = EditProfileForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(username=session['name']).first()
            user.username = form.username.data
            user.email = form.email.data
            user.phone_number = form.phone_number.data
            user.address = form.address.data
            user.buisness_name = form.buisness_name.data
            user.type_of_buisness = form.type_of_buisness.data
            user.abn = form.abn.data
            db.session.add(user)
            db.session.commit()
            session['name'] = form.username.data
            return redirect(url_for('main.profile'))
        return render_template('EditProfile.html', title="Edit Profile", form=form)
    current_user = User.query.filter_by(username=session['name']).first()
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.phone_number.data = current_user.phone_number
    form.address.data = current_user.address
    form.buisness_name.data = current_user.buisness_name
    form.type_of_buisness.data = current_user.type_of_buisness
    form.abn.data = current_user.abn
    return render_template('EditProfile.html', title="Edit Profile", form=form)
'''
Change password page
GET: Display change password template
POST: Validates old password, then assigns the new password
'''
@main.route("/changepassword", methods=['GET', 'POST'])
@login_required
def changepassword():
    form = ChangePasswordForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(username=session['name']).first()
            if user.check_password(form.current_password.data):
                user.set_password(form.new_password.data)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('main.profile'))
            return render_template('ChangePassword.html', form=form)
        return render_template('ChangePassword.html', form=form)
    return render_template('ChangePassword.html', form=form)

'''
Edit listings page
TODO Implement function to edit listings. Currently redirects to profile page for testing purposes
'''
@main.route("/editlisting", methods=['GET', 'POST'])
@login_required
def editlisting():
    return redirect(url_for('main.profile'))

'''
Accepting a listing
PARAMS: listing_id - id corresponding to the database entry
GET: If the user belongs to the listing_id, and the listing has been accepted, then redirects to the chat. Otherwise redirects to map page
POST: Connects user with the listing author if the listing has not already been accepted. Otherwise redirects to map page
'''
@main.route("/acceptlisting/<listing_id>", methods=['GET', 'POST'])
@login_required
def acceptlisting(listing_id):
    listing = Listing.query.filter_by(id=listing_id).first()
    user = User.query.filter_by(username=session['name']).first()
    donor_user = User.query.filter_by(id=listing.user_id).first()
    if (listing.author == user or listing.accepteduser == user) and listing.accepted_listing == True:
        return render_template("AcceptedListing.html", title="Chat", listing=listing)
    if request.method == "POST":
        if listing.accepted_listing == False and listing != None and user.id != donor_user.id: 
            listing.accepted_listing = True
            listing.accepteduser = user
            db.session.add(listing)
            db.session.commit()
            return redirect(url_for('main.acceptlisting', listing_id=listing_id))
        return redirect(url_for('main.map'))
    return redirect(url_for('main.map'))

'''
Get all listings that have been accepted and/or created by that user
GET: Displays active listings
'''
@main.route("/activelistings", methods=['GET'])
@login_required
def activelistings():
    listing = Listing.query.all()
    form = AccessListingForm()
    user = User.query.filter_by(username=session['name']).first()
    return render_template("ActiveListings.html", title="Active listings", Listings=listing, user=user, form=form)

'''
Renders the map and all current listings underneath (current listing=listing that has not yet been accepted)
GET: Displays map and current listings. Each listing is rendered onto the map
'''
@main.route("/map", methods=['GET'])
@login_required
def map():
    listings = Listing.query.all()
    individual = IndividualProduct.query.all()
    form = AcceptListingForm()
    user = User.query.filter_by(username=session['name']).first()
    location_list_json = []
    for listing in listings:
        if listing.accepted_listing == True:
            continue
        location = {}
        if listing.latitude == None or listing.longitude == None:
            listing.latitude = 0.0
            listing.longitude = 0.0
        location["buisness"] = listing.author.buisness_name
        location["address"] = listing.address
        location["lat"] = listing.latitude
        location["lng"] = listing.longitude
        location_list_json.append(location)
    return render_template("Map.html", title="Map", location_list=location_list_json, Listings=listings, IndividualProduct=individual, form=form, user=user)


