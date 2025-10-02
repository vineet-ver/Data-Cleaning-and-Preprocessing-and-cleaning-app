from flask import Flask, render_template, request, redirect, url_for, send_file, flash, session
import pandas as pd
import numpy as np
import os
from werkzeug.utils import secure_filename
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this in production

# Configuration
UPLOAD_FOLDER = 'uploads'
CLEANED_FOLDER = 'cleaned_data'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CLEANED_FOLDER'] = CLEANED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CLEANED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_data(filepath):
    """Load data from CSV or Excel file"""
    try:
        if filepath.endswith('.csv'):
            return pd.read_csv(filepath)
        elif filepath.endswith(('.xlsx', '.xls')):
            return pd.read_excel(filepath)
    except Exception as e:
        return None

def get_column_info(df):
    """Get detailed information about columns"""
    info = {}
    for col in df.columns:
        info[col] = {
            'dtype': str(df[col].dtype),
            'missing_count': df[col].isnull().sum(),
            'missing_percent': round((df[col].isnull().sum() / len(df)) * 100, 2),
            'unique_count': df[col].nunique(),
            'sample_values': df[col].dropna().head(5).tolist()
        }
    return info

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to filename to avoid conflicts
        name, ext = os.path.splitext(filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{name}_{timestamp}{ext}"
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Load and analyze the data
        df = load_data(filepath)
        if df is None:
            flash('Error loading file. Please check the file format.')
            return redirect(url_for('index'))
        
        # Store file info in session
        session['uploaded_file'] = filename
        session['original_shape'] = df.shape
        
        return redirect(url_for('clean_data'))
    else:
        flash('Invalid file type. Please upload CSV or Excel files only.')
        return redirect(url_for('index'))

@app.route('/clean')
def clean_data():
    if 'uploaded_file' not in session:
        flash('Please upload a file first.')
        return redirect(url_for('index'))
    
    filename = session['uploaded_file']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    df = load_data(filepath)
    if df is None:
        flash('Error loading file.')
        return redirect(url_for('index'))
    
    # Get data summary
    column_info = get_column_info(df)
    
    data_preview = {
        'shape': df.shape,
        'columns': df.columns.tolist(),
        'head': df.head().to_html(classes='table table-striped', table_id='data-preview'),
        'info': column_info,
        'duplicates': df.duplicated().sum()
    }
    
    return render_template('clean.html', data=data_preview)

@app.route('/process', methods=['POST'])
def process_data():
    if 'uploaded_file' not in session:
        flash('Please upload a file first.')
        return redirect(url_for('index'))
    
    filename = session['uploaded_file']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    df = load_data(filepath)
    if df is None:
        flash('Error loading file.')
        return redirect(url_for('index'))
    
    original_shape = df.shape
    processing_log = []
    
    try:
        # Handle missing values
        missing_action = request.form.get('missing_action')
        if missing_action == 'drop_rows':
            df = df.dropna()
            processing_log.append(f"Dropped rows with missing values")
        elif missing_action == 'drop_columns':
            df = df.dropna(axis=1)
            processing_log.append(f"Dropped columns with missing values")
        elif missing_action == 'fill_mean':
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())
            processing_log.append(f"Filled missing values with mean for numeric columns")
        elif missing_action == 'fill_median':
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].median())
            processing_log.append(f"Filled missing values with median for numeric columns")
        elif missing_action == 'fill_mode':
            for col in df.columns:
                mode_value = df[col].mode()
                if not mode_value.empty:
                    df[col] = df[col].fillna(mode_value[0])
            processing_log.append(f"Filled missing values with mode for all columns")
        
        # Handle duplicates
        if request.form.get('remove_duplicates'):
            initial_rows = len(df)
            df = df.drop_duplicates()
            removed_duplicates = initial_rows - len(df)
            if removed_duplicates > 0:
                processing_log.append(f"Removed {removed_duplicates} duplicate rows")
        
        # Remove selected columns
        columns_to_remove = request.form.getlist('columns_to_remove')
        if columns_to_remove:
            df = df.drop(columns=columns_to_remove)
            processing_log.append(f"Removed columns: {', '.join(columns_to_remove)}")
        
        # Data type conversions
        for col in df.columns:
            new_type = request.form.get(f'dtype_{col}')
            if new_type and new_type != 'keep':
                try:
                    if new_type == 'numeric':
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                    elif new_type == 'datetime':
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                    elif new_type == 'string':
                        df[col] = df[col].astype(str)
                    elif new_type == 'category':
                        df[col] = df[col].astype('category')
                    processing_log.append(f"Converted {col} to {new_type}")
                except Exception as e:
                    processing_log.append(f"Failed to convert {col} to {new_type}: {str(e)}")
        
        # Save cleaned data
        name, ext = os.path.splitext(filename)
        cleaned_filename = f"{name}_cleaned{ext}"
        cleaned_filepath = os.path.join(app.config['CLEANED_FOLDER'], cleaned_filename)
        
        if cleaned_filename.endswith('.csv'):
            df.to_csv(cleaned_filepath, index=False)
        else:
            df.to_excel(cleaned_filepath, index=False)
        
        # Store results in session
        session['cleaned_file'] = cleaned_filename
        session['processing_log'] = processing_log
        session['final_shape'] = df.shape
        
        return redirect(url_for('download_page'))
        
    except Exception as e:
        flash(f'Error processing data: {str(e)}')
        return redirect(url_for('clean_data'))

@app.route('/download_page')
def download_page():
    if 'cleaned_file' not in session:
        flash('No processed file available.')
        return redirect(url_for('index'))
    
    # Load cleaned data for preview
    cleaned_filename = session['cleaned_file']
    cleaned_filepath = os.path.join(app.config['CLEANED_FOLDER'], cleaned_filename)
    
    df = load_data(cleaned_filepath)
    
    results = {
        'original_shape': session.get('original_shape'),
        'final_shape': session.get('final_shape'),
        'processing_log': session.get('processing_log', []),
        'preview': df.head().to_html(classes='table table-striped') if df is not None else None,
        'filename': cleaned_filename,
        'summary': df.describe().to_html(classes='table table-striped') if df is not None else None
    }
    
    return render_template('download.html', results=results)

@app.route('/download')
def download_file():
    if 'cleaned_file' not in session:
        flash('No processed file available.')
        return redirect(url_for('index'))
    
    filename = session['cleaned_file']
    filepath = os.path.join(app.config['CLEANED_FOLDER'], filename)
    
    return send_file(filepath, as_attachment=True, download_name=filename)

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)