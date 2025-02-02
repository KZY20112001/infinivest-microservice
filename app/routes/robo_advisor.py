from flask import Blueprint, request, jsonify, current_app

from app.services.bank_statement import generate_portfolio
from app.constants import AppConstants 


robo_advisor_bp = Blueprint('robo-advisor', __name__)

@robo_advisor_bp.route('/<bank_name>/generate', methods=['POST'])
def generate_user_portfolio(bank_name:str = None):
    """
    Endpoint to upload, process a bank statement PDF for a specific bank and then returns a specific portfolio style for the user.
    Expects a pdf file in the form-data named 'file'.
    """
    if bank_name not in AppConstants.ALLOWED_BANKS.value:
        return jsonify({'error': 'This bank is not allowed'}), 400
    file = request.files.get('bank_statement')  
    risk_tolerance_level = request.form.get('risk_tolerance_level')
    if not file:
        return jsonify({'error': 'No bank statement file provided'}), 400
    
    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Invalid file type. Please upload a PDF file.'}), 400

    try:
        result = generate_portfolio(file, bank_name, risk_tolerance_level)  
        return jsonify(result.model_dump()), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 406
    except Exception as e:
        return jsonify({'error': 'An error occurred while processing the PDF: ' + str(e)}), 500



@robo_advisor_bp.route('/', methods=['GET'])
def hello(): 
    return "HELLO"