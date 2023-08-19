from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email
from markupsafe import escape #fixes jinja2 escape error

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')

class JobSearchForm(FlaskForm):
    city = StringField('City')
    state = StringField('State')
    # keyword = StringField('Keyword')
    # location = StringField('Location')
    keyword = SelectField('Job Type', choices=[('Class A', 'Class B'), ('Non CDL', 'Any')])
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