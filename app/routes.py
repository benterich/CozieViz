from flask import Blueprint, render_template, request, redirect, url_for, flash
import os
import pandas as pd

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file:
            filepath = os.path.join('data/uploads', file.filename)
            file.save(filepath)
            return redirect(url_for('main.show_columns', filename=file.filename))
    
    return render_template('upload.html')

@main.route('/columns/<filename>')
def show_columns(filename):
    filepath = os.path.join('data/uploads', filename)
    df = pd.read_csv(filepath)
    columns = df.columns.tolist()
    return f"Columns: {', '.join(columns)}"
