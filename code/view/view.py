from typing import Protocol
from flask import render_template, redirect, url_for, request
class View(Protocol):
    def home():
        ...

class Viewer(View):

    @staticmethod
    def home(employees_list):
        return render_template('index.html', employees=employees_list)
    
    @staticmethod
    def schedule():
        return render_template('schedule.html')
    
    @staticmethod
    def register():
        return render_template('register.html')

    @staticmethod
    def login():
        return redirect(url_for('login'))
    
    @staticmethod
    def login_correct():
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('index'))
    
    @staticmethod
    def add_employee():
        return render_template('add_employee.html')
    
    @staticmethod
    def manage_shifts(shifts):
        return render_template('manage_shifts.html', shifts)

    @staticmethod   
    def redirect():
        return redirect('/')