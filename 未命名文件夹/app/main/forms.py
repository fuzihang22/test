#Flask mega tutorial - https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DecimalField, TextAreaField, FieldList, FormField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from .models import User

#Login form used in routes.py
class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    rem_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SignUpForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()]) #TODO change to proper phone number type
    address = StringField('Address', validators=[DataRequired()]) #TODO change to proper address type 
    buisness_name = StringField('Buisness Name', validators=[DataRequired()])
    type_of_buisness = SelectField("Type", choices=["Donor", "Collector"])
    abn = StringField('ABN', validators=[DataRequired()])

    confirm_password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class CreateListingEntryForm(FlaskForm):
    quantity = DecimalField('Quantity')
    description = StringField('Description')
    category = SelectField("Category", choices=["Bread", "Fruit", "Vegetables", "Dairy", "Other"]) #TODO Add more food categories

class CreateListingForm(FlaskForm):
    product_list = FieldList(FormField(CreateListingEntryForm), min_entries=1)
    address_for_pickup = TextAreaField('Address', validators=[DataRequired()]) #TODO Create proper address field
    abn = TextAreaField('ABN', validators=[DataRequired()])
    submit = SubmitField('Post')

class EditProfileForm(FlaskForm):
    username = StringField('Name')
    email = StringField('Email')
    phone_number = StringField('Phone Number') #TODO change to proper phone number type
    address = StringField('Address') #TODO change to proper address type 
    buisness_name = StringField('Buisness Name')
    type_of_buisness = SelectField("Type", choices=["Donor", "Collector"])
    abn = StringField('ABN')
    submit = SubmitField('Save')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Repeat New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Save')