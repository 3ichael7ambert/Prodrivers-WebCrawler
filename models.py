"""SQLAlchemy models for Warbler."""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class Driver(db.Model):
    id = db.Column(db.String, primary_key=True)
    firstName = db.Column(db.String)
    lastName = db.Column(db.String)
    username = db.Column(db.String)
    password = db.Column(db.String)
    driverType = db.Column(db.String)
    currentAvailability = db.Column(db.String)
    isAssigned = db.Column(db.Boolean)

class Client(db.Model):
    id = db.Column(db.String, primary_key=True)
    jobName = db.Column(db.String)
    jobDescription = db.Column(db.String)
    jobSchedule = db.Column(db.String)
    jobRateOfPay = db.Column(db.String)
    otherJobDetails = db.Column(db.String)
    username = db.Column(db.String)
    password = db.Column(db.String)
    companyID = db.Column(db.String)

class Dispatcher(db.Model):
    id = db.Column(db.String, primary_key=True)
    firstName = db.Column(db.String)
    lastName = db.Column(db.String)
    username = db.Column(db.String)
    password = db.Column(db.String)

class Company(db.Model):
    id = db.Column(db.String, primary_key=True)
    companyName = db.Column(db.String)

class Manager(db.Model):
    id = db.Column(db.String, primary_key=True)
    firstName = db.Column(db.String)
    lastName = db.Column(db.String)
    username = db.Column(db.String)
    password = db.Column(db.String)
    companyID = db.Column(db.String)

class HiddenJob(db.Model):
    id = db.Column(db.String, primary_key=True)
    jobName = db.Column(db.String)
    jobDescription = db.Column(db.String)
    jobSchedule = db.Column(db.String)
    jobRateOfPay = db.Column(db.String)
    otherJobDetails = db.Column(db.String)
    isHidden = db.Column(db.Boolean)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
