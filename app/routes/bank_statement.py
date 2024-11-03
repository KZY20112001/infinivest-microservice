from flask import Blueprint, request, jsonify, current_app

from app.services.bank_statement import classify_profile
from app.constants import AppConstants 


bank_statement_bp = Blueprint('bank_statement', __name__)

@bank_statement_bp.route('/<bank_name>/classify', methods=['POST'])
def classify_user_profile(bank_name:str = None):
    """
    Endpoint to upload, process a bank statement PDF for a specific bank and then returns a specific portfolio style for the user.
    Expects a pdf file in the form-data named 'file'.
    """
    
    if bank_name not in AppConstants.ALLOWED_BANKS.value:
        return jsonify({'error': 'This bank is not allowed'}), 400
 
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No bank statement file provided'}), 400
    
    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Invalid file type. Please upload a PDF file.'}), 400

    try:
        result = classify_profile(file, bank_name)  # Pass bank_name to processing function
        return jsonify({'category': result}), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 406
    except Exception as e:
        return jsonify({'error': 'An error occurred while processing the PDF: ' + str(e)}), 500



@bank_statement_bp.route('/')
def hello(): 
    openai_api_key = current_app.config['OPENAI_API_KEY']

    print(f"OPENAI_API_KEY: {openai_api_key}")
    return "HELLO"