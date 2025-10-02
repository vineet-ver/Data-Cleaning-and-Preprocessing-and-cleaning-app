# Flask Data Preprocessing & Cleaning Web Application

A comprehensive web application built with Flask that allows users to upload data files (CSV, Excel), analyze data quality, apply various cleaning operations, and download the processed results.

## Features

### 🔧 **Data Processing Capabilities**
- **File Support**: CSV, Excel (.xlsx, .xls) files up to 16MB
- **Missing Value Handling**: Drop rows/columns, fill with mean/median/mode
- **Duplicate Removal**: Identify and remove duplicate rows
- **Data Type Conversion**: Convert between numeric, string, datetime, category types
- **Column Management**: Remove unwanted columns
- **Statistical Analysis**: Generate data summaries and previews

### 🎨 **User Interface**
- **Modern Design**: Bootstrap-based responsive UI with gradient backgrounds
- **Interactive Forms**: Dynamic form validation and visual feedback
- **Data Visualization**: Table previews, progress bars for missing data
- **Step-by-step Workflow**: Upload → Analyze → Clean → Download

### 📊 **Analysis Features**
- Data shape and quality overview
- Column-wise statistics (missing values, data types, unique counts)
- Sample value previews
- Processing log with detailed steps performed

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Project Structure
Create the following folder structure:
```
/data_preprocessing_app
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── /templates            # HTML templates
│   ├── base.html         # Base template with styling
│   ├── index.html        # Upload page
│   ├── clean.html        # Data analysis & cleaning options
│   └── download.html     # Results & download page
├── /uploads              # Temporary uploaded files (created automatically)
└── /cleaned_data         # Processed files (created automatically)
```

### Step 3: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

## How to Use

### 1. **Upload Your Data**
- Navigate to the home page
- Click "Choose your data file" and select a CSV or Excel file
- Click "Upload & Analyze Data"

### 2. **Review Data Quality**
- View data overview (rows, columns, duplicates, missing values)
- Examine data preview and column information
- Check missing value percentages and data types

### 3. **Configure Cleaning Options**
- **Missing Values**: Choose how to handle missing data
  - Keep as-is
  - Drop rows/columns with missing values
  - Fill with statistical measures (mean, median, mode)
- **Duplicates**: Option to remove duplicate rows
- **Column Operations**: Select columns to remove
- **Data Types**: Convert column data types as needed

### 4. **Process & Download**
- Click "Process Data" to apply selected cleaning operations
- Review processing summary and cleaned data preview
- Download the cleaned dataset
- View detailed processing log

## Technical Details

### Backend (Flask)
- **Framework**: Flask 2.3.3
- **Data Processing**: Pandas 2.0.3, NumPy 1.24.3
- **File Handling**: Werkzeug for secure file uploads
- **Excel Support**: openpyxl, xlrd for Excel file processing

### Frontend
- **CSS Framework**: Bootstrap 5.1.3
- **Icons**: Font Awesome 6.0.0
- **Design**: Modern gradient design with responsive layout
- **Interactive Elements**: Dynamic form updates, progress indicators

### Security Features
- Secure filename handling
- File type validation
- File size limits (16MB max)
- Session management for user data

### Data Processing Operations
1. **Missing Value Imputation**:
   - Statistical imputation (mean, median, mode)
   - Complete case analysis (row/column deletion)

2. **Data Quality Improvement**:
   - Duplicate detection and removal
   - Data type optimization
   - Column selection and filtering

3. **Analysis & Reporting**:
   - Comprehensive data profiling
   - Processing audit trail
   - Statistical summaries

## Configuration Options

### File Upload Settings
- **Supported formats**: CSV, XLSX, XLS
- **Maximum file size**: 16MB (configurable in app.py)
- **Upload directory**: `/uploads` (configurable)
- **Output directory**: `/cleaned_data` (configurable)

### Security Settings
- **Secret key**: Change `app.secret_key` in production
- **Session management**: Flask sessions for user state
- **File validation**: Strict file type checking

## Deployment Considerations

### For Production Use
1. **Change Secret Key**: Update `app.secret_key` to a secure random value
2. **Environment Variables**: Use environment variables for sensitive config
3. **File Cleanup**: Implement periodic cleanup of temporary files
4. **Error Handling**: Add comprehensive error logging
5. **Security**: Add CSRF protection and input validation
6. **Performance**: Consider adding file size and processing limits

### Cloud Deployment
- Compatible with platforms like Heroku, Railway, Render
- Requires minimal configuration changes
- Stateless design suitable for containerization

## Troubleshooting

### Common Issues
- **File Upload Errors**: Check file size and format
- **Processing Failures**: Verify data format and column types
- **Memory Issues**: Large files may require increased memory limits

### File Compatibility
- **CSV**: UTF-8 encoding recommended
- **Excel**: Modern .xlsx format preferred over legacy .xls
- **Special Characters**: Ensure proper encoding for international data

## Extension Ideas

### Additional Features You Could Add
- **Advanced Analytics**: Correlation analysis, outlier detection
- **Data Visualization**: Charts and graphs for data exploration
- **Export Formats**: JSON, Parquet, SQL export options
- **Batch Processing**: Handle multiple files simultaneously
- **Data Validation**: Custom validation rules and constraints
- **API Endpoints**: RESTful API for programmatic access

This application provides a solid foundation for data preprocessing workflows and can be easily extended with additional features based on specific requirements.