from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextAreaField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length
from markupsafe import escape #fixes jinja2 escape error
from models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[Length(min=6)])
    remember_me = BooleanField('Remember Me')


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
    state = StringField('State')
    keyword = StringField('Keyword')

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DecimalField, BooleanField
from wtforms.validators import DataRequired

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
    endorsements = SelectMultipleField('Required Endorsements', choices=[
        ('tanker', 'Tanker Endorsement'),
        ('hazmat', 'Hazmat Endorsement'),
        ('doubles_triples', 'Doubles/Triples Endorsement'),
        ('passenger', 'Passenger Endorsement')
    ])
    job_schedule = StringField('Job Schedule', validators=[DataRequired()])


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