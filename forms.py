from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextAreaField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Email, Length
from wtforms.widgets import CheckboxInput, ListWidget
from wtforms.fields import FieldList

from markupsafe import escape #fixes jinja2 escape error
from models import User

#######################################################################################################################

# List of state abbreviations
state_abbreviations = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
                       "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
                       "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                       "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                       "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

#######################################################################################################################
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[Length(min=6)])
    # remember_me = BooleanField('Remember Me')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password_hash = PasswordField('Password', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    user_role = SelectField('User Role', choices=[('', 'Select User Role'), ('driver', 'Driver'), ('client', 'Client'), ('dispatcher', 'Dispatcher')],
                            validators=[DataRequired()])
    license_type = SelectField('License Type', choices=[('', 'Select License Type'), ('class_a', 'Class A'), ('class_b', 'Class B'), ('non_cdl', 'Non-CDL')],
                               render_kw={'style': 'display: none;'})
    company_name = StringField('Company Name', render_kw={'style': 'display: none;'})



class JobSearchForm(FlaskForm):
    city = StringField('City')
    state = SelectField('State', choices=[(state, state) for state in state_abbreviations])
    keyword = StringField('Keyword')


class JobPostForm(FlaskForm):
    job_title = StringField('Job Title', validators=[DataRequired()])
    job_description = TextAreaField('Job Description', validators=[DataRequired()])
    job_duties = StringField('Job Duties', validators=[DataRequired()])
    job_state = StringField('State', validators=[DataRequired()])
    job_city = StringField('City', validators=[DataRequired()])
    job_payrate = DecimalField('Pay Rate ($)', validators=[DataRequired()])
    job_class = SelectField('Class', choices=[
        ('class_a', 'Class A'), 
        ('class_b', 'Class B'), 
        ('class_c', 'Class C'), 
        ('non_cdl', 'Non-CDL')
    ], validators=[DataRequired()])


class JobEditForm(FlaskForm):
    job_title = StringField('Job Title', validators=[DataRequired()])
    job_description = TextAreaField('Job Description', validators=[DataRequired()])

class UserProfileForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password')
    confirm_new_password = PasswordField('Confirm New Password')



    ########################################################################################################
class DriverDashboardForm(FlaskForm):
    update_profile = SubmitField('Update Profile')
    remove_job = SubmitField('Remove Job')

class ClientDashboardForm(FlaskForm):
    remove_driver = SubmitField('Remove Driver')
    delete_job = SubmitField('Delete Job')

class DispatchDashboardForm(FlaskForm):
    pass

    ########################################################################################################

class UserEditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Save Changes')
    
class DriverEditForm(UserEditForm):
    # Add fields specific to the driver profile here
    license_number = StringField('License Number', validators=[DataRequired(), Length(max=20)])
    car_make = StringField('Car Make', validators=[DataRequired(), Length(max=50)])
    car_model = StringField('Car Model', validators=[DataRequired(), Length(max=50)])

class ClientEditForm(UserEditForm):
    # Add fields specific to the client profile here
    company_name = StringField('Company Name', validators=[DataRequired(), Length(max=100)])

class DispatcherEditForm(UserEditForm):
    # Add fields specific to the dispatcher profile here
    department = StringField('Department', validators=[DataRequired(), Length(max=50)])