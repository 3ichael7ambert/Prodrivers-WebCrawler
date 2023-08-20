from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email
from markupsafe import escape #fixes jinja2 escape error
from models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    def validate(self, extra_validators=None):
        if not super(LoginForm, self).validate():
            return False
        
        # Check if a user with the provided username exists
        user = User.query.filter_by(username=self.username.data).first()
        if user is None:
            self.username.errors.append('Invalid username or password.')
            return False
        
        # Check if the provided password is correct
        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid username or password.')
            return False

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    user_role = SelectField('User Role', choices=[('', 'Select User Role'), ('driver', 'Driver'), ('client', 'Client'), ('dispatcher', 'Dispatcher')],
                            validators=[DataRequired()])
    license_type = SelectField('License Type', choices=[('', 'Select License Type'), ('class_a', 'Class A'), ('class_b', 'Class B'), ('non_cdl', 'Non-CDL')],
                               render_kw={'style': 'display: none;'})
    company_name = StringField('Company Name', render_kw={'style': 'display: none;'})
    def validate(self, extra_validators=None):
        initial_validation = super().validate()
        if not initial_validation:
            return False
        
        # Check if the username is already in use
        existing_user_with_username = User.query.filter_by(username=self.username.data).first()
        if existing_user_with_username:
            self.username.errors.append('Username is already in use.')
            return False
        
        # Check if the email is already in use
        existing_user_with_email = User.query.filter_by(email=self.email.data).first()
        if existing_user_with_email:
            self.email.errors.append('Email is already in use.')
            return False
        return True


class JobSearchForm(FlaskForm):
    city = StringField('City')
    state = StringField('State')
    # keyword = StringField('Keyword')
    # location = StringField('Location')
    #keyword = SelectField('Job Type', choices=[('Class A', 'Class B'), ('Non CDL', 'Any')])
    keyword = StringField('Keyword')
    # salary_range = SelectField('Salary Range', choices=[('any', 'Any'), ('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])

class JobPostForm(FlaskForm):
    job_title = StringField('Job Title', validators=[DataRequired()])
    job_description = TextAreaField('Job Description', validators=[DataRequired()])
    qualifications = TextAreaField('Qualifications', validators=[DataRequired()])

class JobEditForm(FlaskForm):
    job_title = StringField('Job Title', validators=[DataRequired()])
    job_description = TextAreaField('Job Description', validators=[DataRequired()])

class UserProfileForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password')
    confirm_new_password = PasswordField('Confirm New Password')