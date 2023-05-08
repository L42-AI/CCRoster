from flask import Flask, render_template, request, redirect, jsonify
from model.representation.data_objects import Employee, Availability, Shift
from model.data.assign import employee_list as imported_employee_list  # Rename the imported list to avoid conflicts
from model.data.assign import shift_list as imported_shift_list
from datetime import datetime
import json
import database

#http://127.0.0.1:5000

app = Flask(__name__, template_folder='view/templates', static_folder='view/static')

def create_employee_list():
    return imported_employee_list

employee_list = create_employee_list()

@app.route('/')
def index():
    return render_template('index.html', employees=employee_list, shifts=imported_shift_list)

@app.route('/add_employee')
def add_employee_form():
    return render_template('add_employee.html')

@app.route('/manage_shifts')
def manage_shifts_page():
    return render_template('manage_shifts.html', shifts=imported_shift_list)

@app.route('/delete_shift', methods=['POST'])
def delete_shift():
    shift_id = id
    print(shift_id)
    
    # update shift list
    imported_shift_list = [shift for shift in imported_shift_list if shift.id != shift_id]
    return jsonify({'result': 'success'}) 


@app.route('/save_shift/', methods=['POST'])
def save_shift():
    start_str = request.form.get('start')
    end_str = request.form.get('end')
    shift_type = request.form.get('shift_type')

    # Convert the startStr and endStr into datetime.datetime objects
    start = datetime.strptime(start_str[:-6], '%Y-%m-%dT%H:%M:%S')
    end = datetime.strptime(end_str[:-6], '%Y-%m-%dT%H:%M:%S')
    id = len(imported_shift_list)

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

if __name__ == '__main__':
    app.run(debug=True)
