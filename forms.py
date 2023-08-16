from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email
from markupsafe import escape #fixes jinja2 escape error

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')

class JobSearchForm(FlaskForm):
    location = StringField('Location')
    job_type = SelectField('Job Type', choices=[('full_time', 'Full Time'), ('part_time', 'Part Time')])
    salary_range = SelectField('Salary Range', choices=[('any', 'Any'), ('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])

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