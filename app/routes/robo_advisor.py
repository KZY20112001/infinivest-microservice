from flask import Blueprint, request, jsonify

from app.services import generate_portfolio, generate_asset_allocation
from app.constants import AppConstants 


robo_advisor_bp = Blueprint('robo-advisor', __name__)

@robo_advisor_bp.route('/generate/categories', methods=['POST'])
def generate_portfolio_handler(bank_name:str = None):
    """
    Endpoint to upload, process a bank statement PDF for a specific bank and then returns a specific portfolio style for the user.
    Expects a pdf file in the form-data named 'file'.
    """
    file = request.files.get('bank_statement')  
    bank_name = request.form.get('bank_name')
    risk_tolerance_level = request.form.get('risk_tolerance_level')
    
    if bank_name not in AppConstants.ALLOWED_BANKS.value:
        return jsonify({'error': 'This bank is not allowed'}), 400
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

@robo_advisor_bp.route('/generate/assets', methods=['POST'])
def generate_asset_allocation_handler():
    """
    Endpoint to generate the asset split for a given category and total percentage
    """
    data = request.get_json()
    category = data.get("category")
    percentage = data.get("percentage")
    
    if not category or category not in AppConstants.ALLOWED_PORTFOLIO_CATEGORIES.value:
        return jsonify({"error": "Invalid category"}), 400
    
    if not isinstance(percentage, (int, float)) or percentage < 0 or percentage > 100:
        return jsonify({"error": "Invalid percentage"}), 400
    try:
        result = generate_asset_allocation(category, str(percentage))
        return jsonify(result.model_dump()), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 406
    except RuntimeError as re:
        return jsonify({'error': str(re)}), 500
    except Exception as e:
        return jsonify({'error': 'An error occurred while generating asset allocation: ' + str(e)}), 500

