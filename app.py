from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape, Markup #fixes jinja2 escape error

from models import db, Driver, Client, Dispatcher, Company, Manager, HiddenJob
from forms import LoginForm

from webcrawl import scrape_job_data

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SeKRuT'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///driver_jobs_db'
db = SQLAlchemy(app)

# Define your models here using SQLAlchemy
