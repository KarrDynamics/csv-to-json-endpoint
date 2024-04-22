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


@app.route('/json-endpoint', methods=['GET'])
def json_endpoint():
    print("json_endpoint function is called")  # Temporary debug print

    try:
        json_file_path = './uploads/converted.json'

        if not os.path.exists(json_file_path):
            return jsonify({"error": "File not found"}), 404

        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        # Get all query parameters from the request
        query_params = request.args

        # Filter data based on the provided query parameters
        filtered_data = data
        for key, value in query_params.items():
            filtered_data = [item for item in filtered_data if item.get(key) == value]

        return jsonify(filtered_data), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500


@app.route('/json-endpoint', methods=['GET'])
def get_filtered_data():
    print("get_filtered_data function is called")  # Temporary debug print

    try:
        json_file_path = './uploads/converted.json'

        if not os.path.exists(json_file_path):
            return jsonify({"error": "File not found"}), 404

        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        # Get query parameters
        filters = {key.lower(): value for key, value in request.args.items()}

        print(f"Received filters: {filters}")  # Debug print

        # Filter data based on query parameters
        filtered_data = [item for item in data if all(item.get(key) == value for key, value in filters.items())]

        print(f"Filtered data count: {len(filtered_data)}")  # Debug print
        print(f"Filtered data: {filtered_data}")  # Debug print

        return jsonify(filtered_data), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500