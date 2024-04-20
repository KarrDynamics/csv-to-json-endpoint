from flask import render_template, request, jsonify, send_from_directory
import os
from app import app
from werkzeug.utils import secure_filename
import logging
import json
import shutil
import csv

# Set the upload folder
app.config['UPLOAD_FOLDER'] = './uploads'

@app.route('/')
def index():
    try:
        return render_template('upload.html')
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Get the uploaded file
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        file_content = file.read().decode('utf-8')
        
        # Check if the uploaded file is a CSV file
        if file.filename.endswith('.csv'):
            # Convert CSV to JSON
            csv_rows = []
            csv_data = csv.reader(file_content.splitlines())
            headers = next(csv_data)
            for row in csv_data:
                csv_rows.append(dict(zip(headers, row)))
            
            logging.debug("CSV data converted to JSON")
            
            # Save JSON to a file with a consistent name
            json_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'converted.json')
            with open(json_file_path, 'w') as json_file:
                json.dump(csv_rows, json_file)
            
            return jsonify({"message": "File uploaded and converted successfully", "json_file_path": json_file_path}), 200
        
        else:
            return jsonify({"error": "Unsupported file format"}), 400
    
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500


@app.route('/json-endpoint', methods=['GET', 'POST'])
def json_endpoint():
    if request.method == 'POST':
        try:
            # Load JSON from the uploaded file
            json_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'converted.json')
            
            if not os.path.exists(json_file_path):
                return jsonify({"error": "File not found"}), 404
            
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)
            
            return jsonify(data), 200
        
        except Exception as e:
            return jsonify({"error": f"An error occurred: {e}"}), 500
    elif request.method == 'GET':
        try:
            # You can add code here to handle GET requests, for example:
            with open(os.path.join(app.config['UPLOAD_FOLDER'], 'example.json'), 'r') as file:
                data = json.load(file)
            return jsonify(data), 200
        
        except FileNotFoundError:
            return jsonify({"error": "File not found"}), 404
        except Exception as e:
            return jsonify({"error": f"An error occurred: {e}"}), 500
