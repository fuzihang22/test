from flask import Flask, session, request, render_template, url_for, flash, redirect
from .. import login, db
from . import main
from .forms import LoginForm, SignUpForm, CreateListingForm, EditProfileForm, ChangePasswordForm, CreateListingEntryForm
from markupsafe import escape
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from sqlalchemy.sql import func
from .models import User, Listing, IndividualProduct

@main.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = func.now()
        db.session.commit()

#Render home page
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

#Handle user register routing
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

@main.route("/listings", methods=['GET', 'POST'])
@login_required
def listings():
    listings = Listing.query.all()
    individual = IndividualProduct.query.all()
    return render_template('Listings.html', Listing=listings, title="CURRENT LISTINGS", IndividualProduct=individual)


@main.route("/createlisting", methods=['GET', 'POST'])
@login_required
def createlisting():
    form = CreateListingForm()
    if request.method == "POST":
        print(form.validate_on_submit())
        print(form.errors)
        if form.validate_on_submit():
            user = User.query.filter_by(username=session['name']).first()
            listing = Listing(author=user)
            listing.address_for_pickup = form.address_for_pickup.data
            listing.abn = form.abn.data

            for product in form.product_list.data:
                indivdual_product = IndividualProduct(listing=listing)
                indivdual_product.quantity = product['quantity']
                indivdual_product.description = product['description']
                indivdual_product.category = product['category']

                db.session.add(indivdual_product)
                db.session.commit()
                print(indivdual_product.quantity)
                print(indivdual_product.description)
                print(indivdual_product.category)
                
            return redirect(url_for('main.listings'))
        return render_template('CreateListing.html', form=form, title="CREATE LISTING")
    return render_template('CreateListing.html', form=form, title="CREATE LISTING")


@main.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.filter_by(username=session['name']).first()
    listing = Listing.query.filter_by(author=user).all()
    return render_template('Profile.html', title="Profile", user_info=user, Listing=listing)


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


@main.route("/editlisting", methods=['GET', 'POST'])
@login_required
def editlisting():
    #TODO Implement function to edit listings
    return redirect(url_for('main.profile'))