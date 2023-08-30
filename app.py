import os
from flask import Flask, render_template, redirect, url_for, request, flash, session, g
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape # fixes jinja2 escape error
import requests , random
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash


from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Driver, Client, Dispatcher, Company, HiddenJob, User
from forms import LoginForm, RegisterForm, JobSearchForm, JobPostForm, JobEditForm, UserProfileForm, DriverDashboardForm, ClientDashboardForm, DispatchDashboardForm

from webcrawl import scrape_job_data

from werkzeug.utils import secure_filename

from config import DEBUG
from flask_migrate import Migrate
import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

CURR_USER_KEY = "curr_user"


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///driver_jobs_db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = DEBUG #True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

app.config['SECRET_KEY'] = 'SeKRuT'

migrate = Migrate(app, db)

toolbar = DebugToolbarExtension(app)

csrf = CSRFProtect(app)
app.app_context().push()
connect_db(app)
db.create_all() 

# Set up logging
logging.basicConfig(level=logging.DEBUG)

###############################################################################
##Random City Method
# Make a request to the Random User Generator API
response = requests.get('https://randomuser.me/api/?nat=us')
# Parse the response to get the state and city information
data = response.json()
random_state = data['results'][0]['location']['state']
random_city = data['results'][0]['location']['city']
key_param = ''

# Construct the URL with the random state and city
city_param = random_city
state_param = random_state
url = f"https://www.prodrivers.com/jobs/?_city={city_param}&_state={state_param}&_title={key_param}"

job_data = scrape_job_data(f"https://www.prodrivers.com/jobs/?_city={city_param}&_state={state_param}&_title={key_param}") 


###############################################

def get_job_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        return job_data
    else:
        return []
    

def get_state_abbreviation(full_state_name):
    state_mapping = {
        "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
        "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
        "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
        "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
        "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
        "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
        "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
        "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
        "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
        "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
    }
    
    return state_mapping.get(full_state_name, None)

# List of state abbreviations
state_abbreviations = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
                       "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
                       "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                       "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                       "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]




################################################################################################################################################################################################
# User signup/login/logout



@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

@app.before_request
def load_logged_in_user():
    user_id = session.get(CURR_USER_KEY)
    g.user = User.query.get(user_id) if user_id else None




def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    session.pop(CURR_USER_KEY, None)
    g.user = None


# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.check_password(form.password_hash.data):  # Corrected form field name
                do_login(user)
                flash(f"Hello, {user.first_name}!", "success")
                return redirect("/")
            else:
                print("Password doesn't match")  # Debugging
        else:
            print("Username not found")  # Debugging
            flash("Invalid username or password.", 'danger')
    return render_template('login.html', form=form)


# Route for logging out
@app.route('/logout')
#@login_required
def logout():
    #logout_user()
    """Handle logout of user."""
    do_logout()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))



@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user signup.

    Create a new user and add to the DB. Redirect to the home page.

    If the form is not valid, present the form.

    If there is already a user with that username or email: flash message
    and re-present the form.
    """
        
    form = RegisterForm()

    app.logger.debug("Fetching user data...")

    if form.validate_on_submit():

        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Email already registered", 'danger')
            return render_template('register.html', form=form)
        try:
            user = User.signup(
                username=form.username.data,
                password_hash=form.password_hash.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                user_role=form.user_role.data,
                license_type=form.license_type.data,
                company_name=form.company_name.data,
           )

            db.session.add(user)
            db.session.commit()  # Commit here within the try block
            do_login(user)

            return redirect("/")
        
        except IntegrityError:
            db.session.rollback()  # Rollback if there's an exception
            flash("Username or email already taken", 'danger')
            return render_template('register.html', form=form)
    
    else:
        # Handle presenting the form for GET requests
        return render_template('register.html', form=form)

        return render_template('register.html', form=form)




################################################################################################################################################################################################
# General user routes:


def get_random_job_data2():
    # Choose a random state abbreviation from the list
    state_param = random.choice(state_abbreviations)
    
    # Construct the URL with the random state abbreviation
    city_param = ""  # You can specify the city if needed
    url = f"https://www.prodrivers.com/jobs/?_city={city_param}&_state={state_param}"
    
    # Fetch random job data
    job_data = scrape_job_data(url)
    return job_data


def get_random_job_data():
    # Get random city and state
    response = requests.get('https://randomuser.me/api/?nat=us')
    data = response.json()
    random_state = data['results'][0]['location']['state']
    random_city = data['results'][0]['location']['city']
    
    # Map the full state name to its abbreviation
    state_abbreviation = get_state_abbreviation(random_state)

    if state_abbreviation:
        # Construct the URL with the random state abbreviation and city
        city_param = random_city
        state_param = state_abbreviation
        key_param = ''
        url = f"https://www.prodrivers.com/jobs/?_city=&_state={state_param}"

        # Fetch random job data
        job_data = scrape_job_data(url)
        return job_data
    else:
        return []


##################################################################################################################################################################################################

# Route for home page (job board)
@app.route('/')
def main():
    form = LoginForm()
    
    # Get random city and state
    response = requests.get('https://randomuser.me/api/?nat=us')
    data = response.json()
    random_state = data['results'][0]['location']['state']
    random_city = data['results'][0]['location']['city']
    
    # Map the full state name to its abbreviation
    state_abbreviation = get_state_abbreviation(random_state)

    if state_abbreviation:
        # Construct the URL with the random state abbreviation and city
        city_param = random_city
        state_param = state_abbreviation
        key_param = ''
        url = f"https://www.prodrivers.com/jobs/?_city=&_state={state_param}"

        # Fetch random job data
        job_data = scrape_job_data(url)
        
        # Pass the city and state parameters to the template
        return render_template('index.html', form=form, job_data=job_data,
                               city_param=city_param, state_param=state_param)
    else:
        return render_template('index.html', form=form)


@app.route('/home')
def home():
    form = LoginForm()
    
    # Fetch random job data
    job_data = get_random_job_data2()
    
    return render_template('index.html', form=form, job_data=job_data)


@app.route('/profile/<int:user_id>')
def profile(user_id):
    if g.user:
        if g.user.role == 'driver':
            return redirect(url_for('driver_dashboard', username=g.user.username))
        elif g.user.role == 'client':
            return redirect(url_for('client_dashboard', username=g.user.username))
        elif g.user.role == 'dispatcher':
            return redirect(url_for('dispatch_dashboard', username=g.user.username))
        else:
            return redirect(url_for('home')) 



@app.route('/job_board', methods=['GET', 'POST'])
def job_board():
    job_search_form = JobSearchForm()

    if request.method == 'POST':
        city = request.form.get('city')
        state = request.form.get('state')
        keyword = request.form.get('keyword')

        # Construct the URL with user input
        url = f"https://www.prodrivers.com/jobs/?_city={city}&_state={state}&_title={keyword}"
        job_data = scrape_job_data(url)  # Pass the URL to the scrape_job_data function

        return render_template('job_board.html', job_search_form=job_search_form, job_data=job_data)

    return render_template('job_board.html', job_search_form=job_search_form)



def job_search():
    job_search_form = JobSearchForm(request.args)

    if job_search_form.validate_on_submit():
        city_param = job_search_form.city.data
        state_param = job_search_form.state.data
        key_param = job_search_form.keyword.data

        url = f"https://www.prodrivers.com/jobs/?_city={city_param}&_state={state_param}&_title={key_param}"
        job_data = get_job_data(url)

        return render_template('job_board.html', job_search_form=job_search_form, job_data=job_data)
    else:
        return render_template('job_board.html', job_search_form=job_search_form)



# Route for driver dashboard using g.user
@app.route('/driver_dashboard/<username>')
def driver_dashboard(username):
    form = DriverDashboardForm()
    if g.user:
        driver = Driver.query.filter_by(username=username).first()
        return render_template('drivers/driver_dashboard.html', driver=driver)
    else:
        return redirect(url_for('login'))  # Redirect to login if user not logged in


# Route for dispatcher dashboard
@app.route('/dispatch_dashboard/<username>')
#@login_required
def dispatch_dashboard(username):
    form = DispatchDashboardForm()
    # Retrieve dispatcher information based on username and display the dashboard
    jobs_by_company = {} 
    dispatcher = Dispatcher.query.filter_by(username=username).first()
    return render_template(
        'dispatch/dispatch_dashboard.html',
        dispatcher=dispatcher,
        jobs_by_company=jobs_by_company  # Pass the variable to the template
    )

# Route for client dashboard
@app.route('/client_dashboard/<username>')
#@login_required
def client_dashboard(username):
    form = ClientDashboardForm()
    # Retrieve client information based on username and display the dashboard
    client = Client.query.filter_by(username=username).first()
    return render_template('clients/client_dashboard.html', client=client)

# Route for manager dashboard
@app.route('/manager_dashboard/<username>')
#@login_required
def manager_dashboard(username):
    form = LoginForm()
    # Retrieve client information based on username and display the dashboard
    manager = Manager.query.filter_by(username=username).first()
    return render_template('manager_dashboard.html', client=client)

##################################################################################################################################################################################
#JOB LOGIC

@app.route('/post_job', methods=['GET', 'POST'])
def add_job():
    form = JobPostForm()

    if form.validate_on_submit():

        job_title = form.job_title.data
        job_description = form.job_description.data
        job_duties = form.job_duties.data
        job_state = form.job_state.data
        job_city = form.job_city.data
        job_payrate = form.job_payrate.data
        job_class = form.job_class.data
        endorsements = form.endorsements.data
        job_schedule = form.job_schedule.data
        
        flash('Job successfully posted.', 'success')
        return redirect(url_for('job_board'))
    else:
        flash('Form validation failed. Please check your input.', 'danger')

    return render_template('clients/post_job.html', form=form)




# Route for editing a job
@app.route('/edit_job/<job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    job = HiddenJob.query.get(job_id)
    if request.method == 'POST':
        # Process the form data and update the job in the database
        job_title = request.form['job_title']
        job_description = request.form['job_description']
        # Update the job in the database using SQLAlchemy

        # After updating, redirect to the job board to see the updated list of jobs
        return redirect(url_for('job_board'))

    return render_template('edit_job.html', job=job)



@app.route('/accept_job/<int:job_id>/<username>')
def accept_job(job_id, username):
    # Get the driver based on the username
    driver = Driver.query.filter_by(username=username).first()

    if not driver:
        flash('Driver not found', 'danger')
        return redirect(url_for('driver_dashboard', username=username))

    # Get the job based on the job_id
    job = HiddenJob.query.get(job_id)

    if not job:
        flash('Job not found', 'danger')
        return redirect(url_for('driver_dashboard', username=username))

    # Update the job's driver and availability status
    job.current_availability = 'Accepted'
    job.is_assigned = True
    job.current_job = driver.id

    # Add the job to the driver's jobs
    driver_jobs = DriverJob(driver_id=driver.id, job_id=job.id)
    db.session.add(driver_jobs)

    # Commit the changes to the database
    db.session.commit()

    flash('Job accepted successfully', 'success')
    return redirect(url_for('driver_dashboard', username=username))




@app.route('/update_profile')
def update_profile():
    # Logic to update the driver's profile
    # You can also perform other necessary tasks
    return redirect(url_for('driver_dashboard'))

@app.route('/remove_job/<int:job_id>')
def remove_job(job_id):
    # Logic to remove the job from the driver's current job
    # 
    return redirect(url_for('driver_dashboard'))

@app.route('/delete_job/<int:job_id>')
def delete_job(job_id):
    # Logic to delete a job (this should cascade and remove from drivers too)
    # 
    return redirect(url_for('client_dashboard'))

##################################################################################################################################################################################
#NAV

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




###########################################################################################################################################################################

if __name__ == '__main__':
    with app.app_context():
        connect_db(app)
        db.create_all()
    app.run(debug=True)
