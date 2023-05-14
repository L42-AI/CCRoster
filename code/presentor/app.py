from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from model.data.representation.data_classes import Employee, Availability, Shift
from controller.database import download_employees, download_shifts
from datetime import datetime, timedelta
import json
import controller.database as database

import os

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




@login_required
def create_employee_list():
    id = current_user.id
    employee_list = download_employees(id)

    return employee_list

def create_shift_list():
    '''Hier moeten we even over nadenken... willen we altijd alle shifts inladen? of alleen van afgelopen maand en aankomende 3 maanden bijv?'''
    pass


@app.route('/')
@login_required
def index():
    employee_list = create_employee_list()
    print(employee_list)
    return render_template('index.html', employees=employee_list)

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
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/add_employee')
@login_required
def add_employee_form():
    return render_template('add_employee.html')

@app.route('/manage_shifts')
@login_required
def manage_shifts_page():
    shift_list = download_shifts(current_user.id)
    return render_template('manage_shifts.html', shifts=shift_list)

@app.route('/delete_shift', methods=['POST'])
def delete_shift():
    shift_id = id
    print(shift_id)
    
    # update shift list
    shift_list = [shift for shift in shift_list if shift.id != shift_id]
    return jsonify({'result': 'success'}) 


@app.route('/save_shift/', methods=['POST'])
def save_shift():
    start_str = request.form.get('start')
    end_str = request.form.get('end')
    shift_type = request.form.get('shift_type')

    # Convert the startStr and endStr into datetime.datetime objects
    start = datetime.strptime(start_str[:-6], '%Y-%m-%dT%H:%M:%S')
    end = datetime.strptime(end_str[:-6], '%Y-%m-%dT%H:%M:%S')
    id = len(shift_list)

    # Save the shift to your database here
    imported_shift_list.append(Shift(start, end, 1, 1))

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
    employee_list.append(new_employee)

    return redirect('/')

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
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check your username and password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
