from flask import Blueprint, request, jsonify, render_template, redirect, url_for  # type: ignore
import os
from werkzeug.utils import secure_filename  # type: ignore
import openpyxl  # type: ignore

excel_bp = Blueprint('excel', __name__)

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
# Temporary storage for participants' data
participants_data = []

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@excel_bp.route('/upload', methods=['POST'])
def upload_excel():
    global participants_data  # Use the global variable for temporary storage
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Process the Excel file
        try:
            workbook = openpyxl.load_workbook(filepath)
            sheet = workbook.active
            participants_data = []  # Reset the temporary storage

            # Assume the first row is headers
            for row in sheet.iter_rows(min_row=2, values_only=True):  # Skip header row
                participants_data.append({"name": row[0], "department": row[1]})

            # Redirect to the template selection page
            return redirect(url_for('excel.template_selection'))
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "Invalid file type"}), 400

# Frontend Route: Display HTML upload form
@excel_bp.route('/upload-form', methods=['GET'])
def upload_form():
    return render_template('upload_form.html')

# Frontend Route: Template selection page
@excel_bp.route('/template-selection', methods=['GET'])
def template_selection():
    return render_template('template_selection.html')

@excel_bp.route('/customization', methods=['GET'])
def template_customization():
    # Render the template customization page
    return render_template('customization.html')



