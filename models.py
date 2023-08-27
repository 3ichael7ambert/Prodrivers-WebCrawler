from datetime import datetime
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from werkzeug.security import generate_password_hash, check_password_hash

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True,nullable=False,autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    password_hash = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    license_type = db.Column(db.String(50)) 
    company_name = db.Column(db.String(100))  

 
    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('UTF-8')


    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @classmethod
    def signup(cls, username, email, password_hash, first_name, last_name, user_role, license_type=None, company_name=None):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password_hash).decode('UTF-8')
        user = User(
            username=username,
            email=email,
            password_hash=hashed_pwd,
            first_name=first_name,
            last_name=last_name,
            role=user_role,
            license_type=license_type,
            company_name=company_name,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password_hash):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password_hash, password_hash)

            if is_auth:
                return user

        return False


class UserRole(Enum):
    DRIVER = 'driver'
    DISPATCHER = 'dispatcher'
    CLIENT = 'client'

class Driver(db.Model):
    __tablename__ = 'drivers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    first_name = db.Column(db.Integer, db.ForeignKey('user.first_name'), primary_key=True)
    last_name = db.Column(db.Integer, db.ForeignKey('user.last_name'), primary_key=True)
    password_hash = db.Column(db.Integer, db.ForeignKey('user.password_hash'), primary_key=True)
    email = db.Column(db.Integer, db.ForeignKey('user.email'), primary_key=True)
    username = db.Column(db.Integer, db.ForeignKey('user.username'), primary_key=True)
    otherJobDetails = db.Column(db.String)
    companyID = db.Column(db.String)
    driverType = db.Column(db.String)
    currentAvailability = db.Column(db.String)
    isAssigned = db.Column(db.Boolean)

class DriverJob(db.Model):
    __tablename__ = 'driver_job'
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    first_name = db.Column(db.Integer, db.ForeignKey('user.first_name'), primary_key=True)
    last_name = db.Column(db.Integer, db.ForeignKey('user.last_name'), primary_key=True)
    password_hash = db.Column(db.Integer, db.ForeignKey('user.password_hash'), primary_key=True)
    email = db.Column(db.Integer, db.ForeignKey('user.email'), primary_key=True)
    username = db.Column(db.Integer, db.ForeignKey('user.username'), primary_key=True)

    otherJobDetails = db.Column(db.String)
    jobs = db.relationship('Job', back_populates='client')

class Job(db.Model):
    __tablename__ = 'job'
    id = db.Column(db.Integer, primary_key=True)
    jobName = db.Column(db.String)
    jobDescription = db.Column(db.String)
    jobSchedule = db.Column(db.String)
    jobRateOfPay = db.Column(db.String)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id')) 
    client = db.relationship('Client', back_populates='jobs')

class Dispatcher(db.Model):
    __tablename__ = 'dispatchers'
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    first_name = db.Column(db.Integer, db.ForeignKey('user.first_name'), primary_key=True)
    last_name = db.Column(db.Integer, db.ForeignKey('user.last_name'), primary_key=True)
    password_hash = db.Column(db.Integer, db.ForeignKey('user.password_hash'), primary_key=True)
    email = db.Column(db.Integer, db.ForeignKey('user.email'), primary_key=True)

    first_name = db.Column(db.String)
    last_name = db.Column(db.String)

    user = db.relationship('User', backref='dispatcher', uselist=False)

    def __repr__(self):
        return f"<Dispatcher #{self.id}: {self.username}, {self.email}>"

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    companyName = db.Column(db.String)
    name = db.Column(db.String(120), unique=True, nullable=False)
    

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
