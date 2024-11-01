from flask import Blueprint, request, jsonify, current_app

# from app.services.pdf_service import process_bank_statement_pdf

# Create a Blueprint for bank statement-related routes
bank_statement_bp = Blueprint('bank_statement', __name__)

@bank_statement_bp.route('/<string:bank_name>/upload', methods=['POST'])
def upload_bank_statement(bank_name):
    """
    Endpoint to upload and process a bank statement PDF for a specific bank.
    Expects a file in the form-data named 'file'.
    Returns the suggested portfolio style for the user.
    """
    # Check if a file is provided in the request
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file provided'}), 400
    
    # Check if the uploaded file is a PDF
    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Invalid file type. Please upload a PDF file.'}), 403

    # Process the bank statement PDF using the pdf_service
    try:
        # result = process_bank_statement_pdf(file, bank_name)  # Pass bank_name to processing function
        return jsonify({'category': "test"}), 200
    except ValueError as ve:
        # Handle specific value errors, e.g., if the PDF format is incorrect
        return jsonify({'error': str(ve)}), 406
    except Exception as e:
        # Handle any other exceptions raised during PDF processing
        return jsonify({'error': 'An error occurred while processing the PDF: ' + str(e)}), 500

@bank_statement_bp.route('/')
def hello(): 
    openai_api_key = current_app.config['OPENAI_API_KEY']

    print(f"OPENAI_API_KEY: {openai_api_key}")
    return "HELLO"