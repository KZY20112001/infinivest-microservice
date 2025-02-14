from flask import Blueprint, request, jsonify

from app.services import get_latest_price

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
