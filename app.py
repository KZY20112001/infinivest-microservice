# app.py

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    # Check for a valid file extension
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Only PDF files are allowed.'}), 400

    # Save uploaded file
    filename = secure_filename(file.filename)
    temp_path = os.path.join('uploads', filename)
    file.save(temp_path)

    # Process the PDF and analyze data


    # Remove temp file after processing
    os.remove(temp_path)
    portfolio = "test"
    return jsonify({'portfolio': portfolio})

if __name__ == '__main__':
    app.run(debug=True)
