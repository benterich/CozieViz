from flask import Blueprint, render_template, session
from my_project.tab_upload.app_upload import upload
from flask import Blueprint, render_template

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
def home():
    return render_template('home.html')

@dashboard.route('/dashboard')
def show_dashboard():
    return render_template('tab_dashboard.html')

