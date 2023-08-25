from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from werkzeug.security import generate_password_hash, check_password_hash

bcrypt = Bcrypt()
db = SQLAlchemy()

# manager_company_association = db.Table(
#     'manager_company_association',
#     db.Column('manager_id', db.Integer, db.ForeignKey('manager.id')),
#     db.Column('company_id', db.Integer, db.ForeignKey('company.id'))
# )


# User related tables
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    license_type = db.Column(db.String(50)) 
    company_name = db.Column(db.String(100))  

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @classmethod
    def signup(cls, username, email, password, first_name, last_name, user_role, license_type=None, company_name=None):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            first_name=first_name,
            last_name=last_name,
            user_role=user_role,
            license_type=license_type,
            company_name=company_name,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password, remember_me):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class UserRole(Enum):
    DRIVER = 'driver'
    DISPATCHER = 'dispatcher'
    CLIENT = 'client'
    # MANAGER = 'manager'

class Driver(db.Model):
    __tablename__ = 'drivers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    # assigned_manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'))  # Updated this line
    otherJobDetails = db.Column(db.String)
    companyID = db.Column(db.String)
    driverType = db.Column(db.String)
    currentAvailability = db.Column(db.String)
    isAssigned = db.Column(db.Boolean)
    # assigned_manager = db.relationship('Manager', foreign_keys=[assigned_manager_id], back_populates='drivers')

class DriverJob(db.Model):
    __tablename__ = 'driver_job'
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'))
    otherJobDetails = db.Column(db.String)
    manager = db.relationship('Manager', back_populates='clients')
    jobs = db.relationship('Job', back_populates='client')

# Job related tables
class Job(db.Model):
    __tablename__ = 'job'
    id = db.Column(db.Integer, primary_key=True)
    jobName = db.Column(db.String)
    jobDescription = db.Column(db.String)
    jobSchedule = db.Column(db.String)
    jobRateOfPay = db.Column(db.String)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id')) 
    client = db.relationship('Client', back_populates='jobs')
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'))
    job_manager = db.relationship('Manager', back_populates='jobs', uselist=False)
    

# Manager related tables
class Manager(db.Model):
    __tablename__ = 'managers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    firstName = db.Column(db.String)
    lastName = db.Column(db.String)
    drivers = db.relationship('Driver', back_populates='assigned_manager', foreign_keys=[Driver.assigned_manager_id])  # Updated this line
    assigned_manager = db.relationship('Driver', back_populates='assigned_manager', foreign_keys=[Driver.assigned_manager_id], viewonly=True)  # Updated this line
    clients = db.relationship('Client')
    dispatchers = db.relationship('Dispatcher', backref='assigned_manager', lazy=True)     
    companies = db.relationship('Company', secondary=manager_company_association, back_populates='managers')
    jobs = db.relationship('Job', back_populates='job_manager')

class Dispatcher(db.Model):
    __tablename__ = 'dispatchers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    firstName = db.Column(db.String)
    lastName = db.Column(db.String)
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'), nullable=False)
    manager = db.relationship('Manager', backref=db.backref('dispatchers'))

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    companyName = db.Column(db.String)
    name = db.Column(db.String(120), unique=True, nullable=False)
    managers = db.relationship('Manager', secondary=manager_company_association, back_populates='companies')
    

class HiddenJob(db.Model):
    __tablename__ = 'hidden_jobs'
    id = db.Column(db.Integer, primary_key=True)
    jobName = db.Column(db.String)
    jobDescription = db.Column(db.String)
    jobSchedule = db.Column(db.String)
    jobRateOfPay = db.Column(db.String)
    otherJobDetails = db.Column(db.String)
    isHidden = db.Column(db.Boolean)
    

 


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)

