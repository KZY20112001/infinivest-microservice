from flask import Blueprint,  jsonify

from app.services import get_latest_price, get_asset_description

assets_bp = Blueprint('assets', __name__)

@assets_bp.route('/latest-price/<symbol>', methods=['GET'])
def generate_portfolio_handler(symbol:str = None):
    """
    Endpoint to get the latest price of a stock or ETF given the symbol
    """
    if not symbol:
        return jsonify({"error": "Symbol parameter is required"}), 400

    latest_price = get_latest_price(symbol)
    if latest_price == 0:
        return jsonify({"error": f"Could not retrieve price for symbol '{symbol}'"}), 404

    return jsonify(latest_price), 200



@assets_bp.route('/description/<symbol>', methods=['GET'])
def generate_description_handler(symbol:str = None):
    """
    Endpoint to generate the description of a stock or ETF given the symbol
    """
    if not symbol:
        return jsonify({"error": "Symbol parameter is required"}), 400

    description = get_asset_description(symbol)
    if description == "":
        return jsonify({"error": f"Could not retrieve description for symbol '{symbol}'"}), 404
    return jsonify(description), 200
