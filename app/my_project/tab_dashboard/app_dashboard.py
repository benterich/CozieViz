from flask import Blueprint, render_template, session

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
def home():
    return render_template('home.html')

@dashboard.route('/dashboard')
def show_dashboard():
    columns = session.get('columns', [])
    return render_template('tab_dashboard.html', columns=columns)
