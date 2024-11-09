import os
from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data/uploads'
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        # Ensure the file has a valid extension
        if not file.filename.endswith('.csv'):
            flash('Only CSV files are allowed')
            return redirect(request.url)

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return redirect(url_for('show_columns', filename=file.filename))
    
    return render_template('upload.html')

@app.route('/columns/<filename>')
def show_columns(filename):
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        df = pd.read_csv(filepath)
        columns = df.columns.tolist()
        return f"Columns: {', '.join(columns)}"
    except Exception as e:
        return f"An error occurred: {str(e)}"
