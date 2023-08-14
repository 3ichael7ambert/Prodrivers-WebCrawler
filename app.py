from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape # fixes jinja2 escape error
import requests 

from models import db, Driver, Client, Dispatcher, Company, Manager, HiddenJob, User
from forms import LoginForm

from webcrawl import scrape_job_data

from werkzeug.utils import secure_filename

from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user

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

# Create a LoginManager instance
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# Route for home page (job board)
@app.route('/')
def main():
    form = LoginForm()
    return render_template('index.html', form=form)

@app.route('/home')
def home():
    return render_template('index.html', form=form, current_user=current_user)

@app.route('/job_board')
def job_board():
    url = request.args.get('url')  # Get the 'url' query parameter from the URL
    if url:
        job_data = scrape_job_data()  # Use the web crawling function to get job data
        return render_template('job_board.html', job_data=job_data)
    else:
        # Handle the case when 'url' parameter is not provided
        return render_template('job_board.html') 
    

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Check login credentials and authenticate user
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)  # Log in the user
            # Redirect to the appropriate dashboard based on user role
            user_type = get_user_type(user.username)
            if user_type == 'driver':
                return redirect(url_for('driver_dashboard', username=user.username))
            elif user_type == 'client':
                return redirect(url_for('client_dashboard', username=user.username))
            elif user_type == 'dispatcher':
                return redirect(url_for('dispatcher_dashboard', username=user.username))
            elif user_type == 'manager':
                return redirect(url_for('manager_dashboard', username=user.username))
            else:
                flash('Unknown user role', 'danger')
                return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html', form=form)


# Route for logging out
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_role = request.form['user_role'] 

        new_user = User(username=username, password=password, role=user_role)
        db.session.add(new_user)
        db.session.commit()

        # Redirect to the appropriate page after registration
        return redirect(url_for('login'))  

    return render_template('register.html') 



# Route for driver dashboard
@app.route('/driver_dashboard/<username>')
@login_required
def driver_dashboard(username):
    # Retrieve driver information based on username and display the dashboard
    driver = Driver.query.filter_by(username=username).first()
    return render_template('driver_dashboard.html', driver=driver)

# Route for dispatcher dashboard
@app.route('/dispatch_dashboard/<username>')
@login_required
def dispatch_dashboard(username):
    # Retrieve dispatcher information based on username and display the dashboard
    dispatcher = Dispatcher.query.filter_by(username=username).first()
    return render_template('dispatch_dashboard.html', dispatcher=dispatcher)

# Route for client dashboard
@app.route('/client_dashboard/<username>')
@login_required
def client_dashboard(username):
    # Retrieve client information based on username and display the dashboard
    client = Client.query.filter_by(username=username).first()
    return render_template('client_dashboard.html', client=client)

# Route for manager dashboard
@app.route('/manager_dashboard/<username>')
@login_required
def manager_dashboard(username):
    # Retrieve client information based on username and display the dashboard
    manager = Manager.query.filter_by(username=username).first()
    return render_template('manager_dashboard.html', client=client)


# Route for posting a new job
@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        # Process the form data and save the new job to the database
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
    with app.app_context():
        db.create_all()
    app.run(debug=True)
