import os
import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

upload = Blueprint('upload', __name__)

UPLOAD_FOLDER = 'data/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@upload.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if not file.filename.endswith('.csv'):
            flash('Please upload a CSV file')
            return redirect(request.url)
        
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        df = pd.read_csv(filepath)
        session['columns'] = df.columns.tolist()
        #flash(f'File '{file.filename}' uploaded successfully!')
        flash(f'File \'{file.filename}\' uploaded successfully!')

        return redirect(url_for('dashboard.show_dashboard'))
    
    return render_template('tab_upload.html')
