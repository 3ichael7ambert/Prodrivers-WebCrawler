from flask import Flask, render_template, redirect, url_for#, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape # fixes jinja2 escape error
import requests 

from models import db, Driver, Client, Dispatcher, Company, Manager, HiddenJob
from forms import LoginForm

from webcrawl import scrape_job_data

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SeKRuT'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///driver_jobs_db'
db = SQLAlchemy(app)


##Random City Method
# Make a request to the Random User Generator API
response = requests.get('https://randomuser.me/api/?nat=us')
# Parse the response to get the state and city information
data = response.json()
random_state = data['results'][0]['location']['state']
random_city = data['results'][0]['location']['city']

# Construct the URL with the random state and city
city_param = random_city
state_param = random_state
url = f"https://www.prodrivers.com/jobs/?{city_param}&{state_param}"

job_data = scrape_job_data(f"https://www.prodrivers.com/jobs/?{city_param}&{state_param}") 

from flask import request

# Route for home page (job board)
@app.route('/')
def home():
    form = LoginForm()
    return render_template('index.html', form=form)


@app.route('/job_board')
def job_board():
    url = request.args.get('url')  # Get the 'url' query parameter from the URL
    if url:
        job_data = scrape_job_data()  # Use the web crawling function to get job data
        return render_template('job_board.html', job_data=job_data)
    else:
        # Handle the case when 'url' parameter is not provided
        return
    

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Check login credentials and authenticate user
        # Replace this with your authentication logic using the form data
        username = form.username.data
        password = form.password.data
        # Perform authentication and redirect to the appropriate dashboard based on user role

        # Example: If the user is a driver, redirect to driver_dashboard
        return redirect(url_for('driver_dashboard', username=username))

    return render_template('login.html', form=form)

# Route for driver dashboard
@app.route('/driver_dashboard/<username>')
def driver_dashboard(username):
    # Retrieve driver information based on username and display the dashboard
    driver = Driver.query.filter_by(username=username).first()
    return render_template('driver_dashboard.html', driver=driver)

# Route for dispatcher dashboard
@app.route('/dispatch_dashboard/<username>')
def dispatch_dashboard(username):
    # Retrieve dispatcher information based on username and display the dashboard
    dispatcher = Dispatcher.query.filter_by(username=username).first()
    return render_template('dispatch_dashboard.html', dispatcher=dispatcher)

# Route for client dashboard
@app.route('/client_dashboard/<username>')
def client_dashboard(username):
    # Retrieve client information based on username and display the dashboard
    client = Client.query.filter_by(username=username).first()
    return render_template('client_dashboard.html', client=client)

# Route for posting a new job
@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        # Process the form data and save the new job to the database
        # Replace this with your logic to handle the job posting form
        job_title = request.form['job_title']
        job_description = request.form['job_description']
        # Save the job to the database using SQLAlchemy

        # After saving, redirect to the job board to see the updated list of jobs
        return redirect(url_for('job_board'))

    return render_template('post_job.html')

# Route for editing a job
@app.route('/edit_job/<job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    job = HiddenJob.query.get(job_id)
    if request.method == 'POST':
        # Process the form data and update the job in the database
        # Replace this with your logic to handle the job editing form
        job_title = request.form['job_title']
        job_description = request.form['job_description']
        # Update the job in the database using SQLAlchemy

        # After updating, redirect to the job board to see the updated list of jobs
        return redirect(url_for('job_board'))

    return render_template('edit_job.html', job=job)







@app.route('/about')
def about():
    form = LoginForm()
    return render_template('about.html', form=form)

@app.route('/services')
def services():
    form = LoginForm()
    return render_template('services.html', form=form)

@app.route('/contact')
def contact():
    form = LoginForm()
    return render_template('contact.html', form=form)




if __name__ == '__main__':
    app.run(debug=True)
