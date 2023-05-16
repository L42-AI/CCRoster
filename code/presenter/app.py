from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import json
import os

from model.representation.data_classes.employee import Employee
from model.representation.data_classes.availability import Availability
from model.representation.data_classes.shift import Shift
from model.data.database import download_employees, download_shifts
from model.model import Generator
from view.view import Viewer
from presenter.presenter import Presenter
from main_schedule import config_dev as config

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
template_directory = os.path.join(parent_directory, 'view', 'templates')
static_directory = os.path.join(parent_directory, 'view', 'static' )

app = Flask(__name__, template_folder=template_directory, static_folder=static_directory)
app.config['SECRET_KEY'] = 'wouterisdebestehuisgenoot'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=2)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://Jacob:wouterisdebestehuisgenoot@185.224.91.162:3308/rooster'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

with app.app_context():
    db.create_all()

@app.route('/')
@login_required
def index():
    ''' this is the home page, it checks if the user has info stored already
        and downloads it if needed'''
    
    if 'id' not in session:
        session['id'] = current_user.id

    if 'employees' not in session:
        PresenterClass = Presenter(Generator, session['id'])
        session['employees'] = PresenterClass.get_employees()
    return Viewer.home(session['employees'])
    
@app.route('/logout')
@login_required
def logout():
    clear_session()
    logout_user()
    return Viewer.login()
    
@login_required
def clear_session():
    if 'id' in session:
        session.pop('id')
    if 'shifts' in session:
        session.pop('shifts')
    if 'employees' in session:
        session.pop('employees')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!')
        return Viewer.login()
    return Viewer.register()

@app.route('/add_employee')
@login_required
def add_employee_form():
    Viewer.add_employee()

@app.route('/manage_shifts')
@login_required
def manage_shifts_page():
    if 'shifts' not in session:
        PresenterClass = Presenter(Generator, session['id'])
        session['shifts'] = PresenterClass.get_shifts()
    return Viewer.manage_shifts(session['shifts'])

@app.route('/delete_shift', methods=['POST'])
def delete_shift():
    shift_id = id
    
    # update shift list
    session['shifts'] = [shift for shift in session['shifts'] if shift.id != shift_id]
    return jsonify({'result': 'success'}) 


@app.route('/save_shift/', methods=['POST'])
def save_shift():
    start_str = request.form.get('start')
    end_str = request.form.get('end')
    shift_type = request.form.get('shift_type')

    # Convert the startStr and endStr into datetime.datetime objects
    start = datetime.strptime(start_str[:-6], '%Y-%m-%dT%H:%M:%S')
    end = datetime.strptime(end_str[:-6], '%Y-%m-%dT%H:%M:%S')
    id = len(session['shifts'])

    # Save the shift to your database here
    session['shifts'].append(Shift(start, end, 1, 1))

    # Return a success response
    return jsonify({'result': 'success'})

@app.route('/add_employee', methods=['POST'])
def process_employee():
    fname = request.form['fname']
    lname = request.form['lname']
    maximum = int(request.form['maximum'])
    minimum = int(request.form['minimum'])
    wage = float(request.form['wage'])
    level = int(request.form['level'])
    task = request.form['task']
    location = int(request.form['location'])
    availability = proces_availability()
    new_employee = Employee(fname, lname, availability, maximum, minimum, wage, level, task, location)
    session['employees'].append(new_employee)

    return Viewer.redirect()

@app.route('/add_availability/')
def proces_availability():
    availability = []
    availability_json = request.form['availability']
    availability_data = json.loads(availability_json)
    for _, av in enumerate(availability_data):
        start_str = av['start'] 
        end_str = av['end']
        av_start = datetime.strptime(start_str[:-6], '%Y-%m-%dT%H:%M:%S')
        av_end = datetime.strptime(end_str[:-6], '%Y-%m-%dT%H:%M:%S')
        availability.append(Availability(start=av_start, end=av_end))
    return availability

@app.route('/login', methods=['GET', 'POST'])
def login():
    ''' method to log a user in '''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=True)
            return Viewer.login_correct()
        else:
            flash('Login unsuccessful. Please check your username and password.')
    return Viewer.login()

@app.route('/schedule')
@login_required
def schedule():
    return Viewer.schedule()

@app.route('/generate_schedule', methods=['POST'])
@login_required
def generate_schedule():
    ''' generate a schedule'''
    PresenterClass = Presenter(Generator, session['id'])
    PresenterClass.get_schedule(config) # HARDCODED CONFIG SETTINGS

    # for now do nothing with the schedule
    return Viewer.schedule()

