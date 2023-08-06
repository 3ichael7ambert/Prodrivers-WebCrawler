"""SQLAlchemy models for Warbler."""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

#ROLES

class Driver(db.Model):
    id = db.Column(db.String, primary_key=True)
    firstName = db.Column(db.String)
    lastName = db.Column(db.String)
    username = db.Column(db.String)
    password = db.Column(db.String)
    driverType = db.Column(db.String)
    currentAvailability = db.Column(db.String)
    isAssigned = db.Column(db.Boolean) #foreign key

class DriverJob(db.Model):
    # Intermediate table for the many-to-many relationship between Driver and Job
    id = db.Column(db.String, primary_key=True)
    driver_id = db.Column(db.String, db.ForeignKey('driver.id'))
    job_id = db.Column(db.String, db.ForeignKey('job.id'))
    
class Job(db.Model):
    id = db.Column(db.String, primary_key=True)
    jobName = db.Column(db.String)
    jobDescription = db.Column(db.String)
    jobSchedule = db.Column(db.String)
    jobRateOfPay = db.Column(db.String)
    client_id = db.Column(db.String, db.ForeignKey('client.id'))  # Foreign key to Client table

    # Define the relationship between Job and Client tables (Many-to-One)
    client = db.relationship('Client', back_populates='jobs')

class Client(db.Model):
    id = db.Column(db.String, primary_key=True)
    otherJobDetails = db.Column(db.String)
    username = db.Column(db.String)
    password = db.Column(db.String)
    companyID = db.Column(db.String)

    # Define the relationship between Client and Job tables (One-to-Many)
    jobs = db.relationship('Job', back_populates='client')

class Dispatcher(db.Model): #admin
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

    # Define the relationship between Manager and all other tables (One-to-Many)
    drivers = db.relationship('Driver', backref='manager')
    clients = db.relationship('Client', backref='manager')
    dispatchers = db.relationship('Dispatcher', backref='manager')
    companies = db.relationship('Company', backref='manager')
    jobs = db.relationship('Job', backref='manager')

class HiddenJob(db.Model):
    id = db.Column(db.String, primary_key=True)
    jobName = db.Column(db.String)
    jobDescription = db.Column(db.String)
    jobSchedule = db.Column(db.String)
    jobRateOfPay = db.Column(db.String)
    otherJobDetails = db.Column(db.String)
    isHidden = db.Column(db.Boolean)
