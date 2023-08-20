from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from enum import Enum as PyEnum

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class UserRole(Enum):
    DRIVER = 'driver'
    DISPATCHER = 'dispatcher'
    CLIENT = 'client'
    MANAGER = 'manager'

class Driver(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    assigned_manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'))
    otherJobDetails = db.Column(db.String)
    companyID = db.Column(db.String)
    driverType = db.Column(db.String)
    currentAvailability = db.Column(db.String)
    isAssigned = db.Column(db.Boolean)
    assigned_manager = db.relationship('Manager', back_populates='drivers')
    manager = db.relationship('Manager', back_populates='assigned_manager', viewonly=True)

class DriverJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jobName = db.Column(db.String)
    jobDescription = db.Column(db.String)
    jobSchedule = db.Column(db.String)
    jobRateOfPay = db.Column(db.String)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship('Client', back_populates='jobs')

class Client(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'))
    otherJobDetails = db.Column(db.String)
    jobs = db.relationship('Job', back_populates='client')
    manager = db.relationship('Manager', back_populates='clients')  # Update this line

class Manager(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    firstName = db.Column(db.String)
    lastName = db.Column(db.String)
    drivers = db.relationship('Driver', back_populates='assigned_manager')
    assigned_manager = db.relationship('Driver', back_populates='manager', viewonly=True)
    clients = db.relationship('Client', back_populates='manager')
    dispatchers = db.relationship('Dispatcher', backref='manager')    companies = db.relationship('Company', backref='manager')
    jobs = db.relationship('Job', backref='manager')
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'))
    manager = db.relationship('Manager', back_populates='clients')  # Update this line


class Dispatcher(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    firstName = db.Column(db.String)
    lastName = db.Column(db.String)
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'))
    manager = db.relationship('Manager', backref='dispatchers')

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    companyName = db.Column(db.String)

class HiddenJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jobName = db.Column(db.String)
    jobDescription = db.Column(db.String)
    jobSchedule = db.Column(db.String)
    jobRateOfPay = db.Column(db.String)
    otherJobDetails = db.Column(db.String)
    isHidden = db.Column(db.Boolean)
