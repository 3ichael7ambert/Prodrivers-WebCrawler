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

from models import db, connect_db, User, Job ,Driver, Client, Dispatcher, Company, HiddenJob
from forms import LoginForm, RegisterForm, JobSearchForm, JobPostForm, JobEditForm, UserProfileForm, DriverDashboardForm, ClientDashboardForm, DispatchDashboardForm, UserEditForm

from webcrawl import scrape_job_data
from webcrawl_prodrivers import scrape_job_data_prodrivers
from webcrawl_cpc import scrape_job_data_cpc
from webcrawl_trillium import scrape_job_data_trillium

from werkzeug.utils import secure_filename

from config import DEBUG
from flask_migrate import Migrate
import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, aliased

CURR_USER_KEY = "curr_user"


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///driver_jobs_db'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True #False
app.config['SQLALCHEMY_ECHO'] = DEBUG #False #DEBUG #True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "SeKRuT")
app.config['DEBUG'] = False



migrate = Migrate(app, db)

toolbar = DebugToolbarExtension(app)

# # csrf = CSRFProtect(app)
# app.app_context().push()
# connect_db(app)
# db.create_all() 
with app.app_context():
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
url_prodrivers = f"https://www.prodrivers.com/jobs/?_city={city_param}&_state={state_param}&_title={key_param}"
url_cpc = f"https://cpclogistics.com/jobs/us/?search_location={city_param}"
url_trillium = f"https://www.prodrivers.com/jobs/?_city={city_param}&_state={state_param}&_title={key_param}"


job_data = scrape_job_data(f"https://www.prodrivers.com/jobs/?_city={city_param}&_state={state_param}&_title={key_param}")
job_data_prodrivers = scrape_job_data_prodrivers(f"https://www.prodrivers.com/jobs/?_city={city_param}&_state={state_param}&_title={key_param}")
job_data_cpc = scrape_job_data_cpc(f"https://cpclogistics.com/jobs/us/?search_location={city_param}")
job_data_trillium = scrape_job_data_trillium(f"https://www.prodrivers.com/jobs/?_city={city_param}&_state={state_param}&_title={key_param}")

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


def fetch_users_without_jobs(role='driver'):
    # Assuming you have a User model defined
    if role == 'driver':
        # Query for users with the 'driver' role who don't have a job
        users_without_jobs = User.query.filter(
            User.role == 'driver',
            User.current_job_id.is_(None)  # Check if the user doesn't have a job
        ).all()
    else:
        # Handle other roles or customize the query as needed
        users_without_jobs = []

    return users_without_jobs




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
        # url_trillium = f"https://trilliumstaffing.com/jobs/search/?keywords=cdl&location={city_param}"
        # url_cpc = f"https://cpclogistics.com/jobs/us/?search_location={city}"
        # url_prodrivers = f"https://www.prodrivers.com/jobs/?_city=&_state={state_param}"

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
        # url_trillium = f"https://trilliumstaffing.com/jobs/search/?keywords=cdl&location={city_param}"
        # url_cpc = f"https://cpclogistics.com/jobs/us/?search_location={city}"
        # url_prodrivers = f"https://www.prodrivers.com/jobs/?_city=&_state={state_param}"

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

    web_job_data = []  # Initialize web_job_data as an empty list
    db_job_data = None   # Initialize db_job_data as None
    matched_jobs = []    # Initialize matched_jobs as an empty list

    # Define default values for the search parameters
    city = None
    state = None
    keyword = None

    if request.method == 'POST':
        city = request.form.get('city')
        state = request.form.get('state')
        keyword = request.form.get('keyword')

        # Scrape job data from the websites
        urls = [
            f"https://www.prodrivers.com/jobs/?_city=&_state={state}",
            f"https://trilliumstaffing.com/jobs/search/?keywords=cdl&location={city}",
            f"https://cpclogistics.com/jobs/us/?search_location={city}"
        ]

        for url in urls:
            if "prodrivers.com" in url:
                web_job_data.extend(scrape_job_data(url))
            elif "trilliumstaffing.com" in url:
                web_job_data.extend(scrape_job_data_trillium(url))
            elif "cpclogistics.com" in url:
                web_job_data.extend(scrape_job_data_cpc(url)) 

        # Query local database for job data
        db_job_data = Job.query.all() 

        # Filter jobs based on search criteria
        for job in db_job_data:
            city_match = not city or job.job_city == city
            state_match = not state or job.job_state == state
            keyword_match = not keyword or (keyword in job.job_title)

            if city_match or state_match or keyword_match:
                matched_jobs.append(job) 

    return render_template(
        'job_board.html',
        job_search_form=job_search_form,
        web_job_data=web_job_data,
        db_job_data=matched_jobs, 
        city_param=city,
        state_param=state,
        keyword=keyword
    )




#######################################################################################################################################
@app.route('/error')
def error():
    return render_template('error.html')

####################################################################################################################################################################################

# Route for driver dashboard using g.user
@app.route('/driver_dashboard/<username>', methods=['GET', 'POST'])
def driver_dashboard(username):
    form = DriverDashboardForm()
    user = g.user  # Retrieve the user from g.user

    if user:
        user = User.query.filter_by(username=username).first()
        job = Job.query.filter_by(driver_id=user.id).first()  # Use driver_id here

        # Inside driver_dashboard function
        if request.method == 'POST' and form.validate_on_submit():
            if job:
                # Remove the current g.user's ID from the driver_id column of the current job
                job.driver_id = None

                # Clear the current_job_id from the users table for the current g.user
                user.current_job_id = None

                # Commit the changes to the database
                db.session.commit()

                flash('Job removed successfully.', 'success')
                return redirect(url_for('driver_dashboard', username=username))  # Include the 'username' parameter

            flash('No job associated with the user.', 'warning')
            return redirect(url_for('driver_dashboard', username=username))  # Include the 'username' parameter

        # Render the template with the 'user' and 'job' variables
        return render_template('drivers/driver_dashboard.html', user=user, job=job, driver_dashboard_form=form)

    return redirect(url_for('login'))





# Route for dispatcher dashboard
@app.route('/dispatch_dashboard/<username>')
def dispatch_dashboard(username):
    form = DispatchDashboardForm()
    
    # Retrieve dispatcher information based on username and role
    dispatcher = User.query.filter_by(username=username, role='dispatcher').first()

    if dispatcher:
        dispatcher_user_id = dispatcher.id
        
        # Create aliases for the User table for client and driver joins
        ClientUser = aliased(User)
        DriverUser = aliased(User)
        
        # Fetch all jobs from the Job table and join with the User table to get client and driver information
        all_jobs = db.session.query(
            Job,
            ClientUser.username.label('client_name'),
            DriverUser.username.label('driver_name')
        ) \
        .outerjoin(ClientUser, ClientUser.id == Job.client_id) \
        .outerjoin(DriverUser, DriverUser.id == Job.driver_id) \
        .all()
        
        # Organize jobs by the client_id column from the Job table
        jobs_by_client = {}
        for job, client_name, driver_name in all_jobs:
            if job.client_id not in jobs_by_client:
                jobs_by_client[job.client_id] = []
            jobs_by_client[job.client_id].append((job, client_name, driver_name))
        
        # List every driver that has an empty current_job_id value from the User table
        drivers_without_jobs = User.query.filter(User.role == 'driver', User.current_job_id.is_(None)).all()
        
        # List every job that has an empty value in the driver_id column of the Job table
        empty_jobs_without_driver = Job.query.filter(Job.driver_id.is_(None)).all()
        
        return render_template(
            'dispatch/dispatch_dashboard.html',
            dispatcher=dispatcher,
            all_jobs=all_jobs,
            jobs_by_client=jobs_by_client,
            drivers_without_jobs=drivers_without_jobs,
            dispatcher_user_id=dispatcher_user_id,
            empty_jobs_without_driver=empty_jobs_without_driver
        )
    
    flash('Dispatcher not found', 'danger')
    return redirect(url_for('main'))






# Route for client dashboard
@app.route('/client_dashboard/<username>')
def client_dashboard(username):
    form = ClientDashboardForm()
    # Check if the user is authenticated and has the appropriate role
    if g.user and g.user.role == 'client':
        # Retrieve client information based on the currently logged-in user
        user_id = g.user.id

        # Attempt to query the client information
        client = User.query.filter_by(id=user_id).first()


        # Query the jobs that match the user's id as the client_id
        all_jobs = Job.query.filter_by(client_id=user_id).all()

        return render_template('clients/client_dashboard.html', client=client, all_jobs=all_jobs)
    else:
        if g.user.role == 'driver':
            return redirect(url_for('driver_dashboard', username=g.user.username))
        elif g.user.role == 'client':
            return redirect(url_for('client_dashboard', username=g.user.username))
        elif g.user.role == 'dispatcher':
            return redirect(url_for('dispatch_dashboard', username=g.user.username))
        else:
            return redirect(url_for('home')) 


# Route for manager dashboard
@app.route('/manager_dashboard/<username>')
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
        if g.user:
            user_id = g.user.id  
        else:
            user_id = None

        new_job = Job(
            job_title=job_title,
            job_description=job_description,
            job_duties=job_duties,
            job_state=job_state,
            job_city=job_city,
            job_payrate=job_payrate,
            job_class=job_class,
            client_id=user_id,  
            driver_id=None
            
        )

        db.session.add(new_job)
        db.session.commit()

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




@app.route('/accept_job/<username>', methods=['POST'])
def accept_job(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('driver_dashboard', username=username))

    # Extract job data from the form
    job_id = request.form['job_id']
    job_title = request.form['job_title']
    job_description = request.form['job_description']
    job_state = request.form['job_state']
    job_city = request.form['job_city']

    # Create a new Job instance with the extracted data
    new_job = Job(
        job_title=job_title,
        job_description=job_description,
        job_state=job_state,
        job_city=job_city,
    )

    # Add the new job entry to the database
    db.session.add(new_job)
    db.session.commit()

    # Assign the new job to the current user
    new_job.driver_id = user.id
    user.current_job_id = new_job.id

    # Update the changes in the database
    db.session.add(new_job)
    db.session.add(user)
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

@app.route('/delete_job/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    # Logic to delete a job
    job = Job.query.get(job_id)
    if job:
        # Get the user associated with this job
        user = User.query.get(job.client_id)
        
        # Update the user's current_job_id to None
        user.current_job_id = None

        # Remove the job from the database
        db.session.delete(job)
        db.session.commit()

    # Redirect to the client dashboard with the username parameter
    return redirect(url_for('client_dashboard', username=user.username))

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

@app.route('/edit_driver/<int:user_id>', methods=['GET', 'POST'])
def edit_driver(user_id):
    # Fetch the driver's data and create a form

    form = UserEditForm()

    if form.validate_on_submit():


        return render_template('drivers/edit_driver.html', form=form, user_id=user_id)

@app.route('/edit_client/<int:user_id>', methods=['GET', 'POST'])
def edit_client(user_id):
    user = User.query.get(user_id)
    form = YourClientEditForm()  # Create an instance of the form
    
    if form.validate_on_submit():
        # Process the form data and update the user's information
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        
        db.session.commit()
        flash('Client information updated successfully', 'success')
        return redirect(url_for('client_dashboard', username=user.username))
    
    # Render the template with the form
    return render_template('edit_client.html', user=user, form=form)

@app.route('/edit_dispatcher/<int:user_id>', methods=['GET', 'POST'])
def edit_dispatcher(user_id):
    # Fetch the dispatcher's data and create a form
    form = YourDispatcherEditForm()

    if form.validate_on_submit():


        return render_template('dispatch/edit_dispatch.html', form=form, user_id=user_id)

###########################################################################################################################################################################

if __name__ == '__main__':
    with app.app_context():
        connect_db(app)
        db.create_all()
    app.run(debug=True)
