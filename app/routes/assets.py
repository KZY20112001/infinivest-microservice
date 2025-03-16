from flask import Blueprint,  jsonify

from app.services import get_latest_price, get_asset_description, get_price_history, get_assets

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


@assets_bp.route('/price-history/<symbol>', methods=['GET'])
def get_asset_price_history(symbol:str = None):
    """
    Endpoint to get the price history of a stock or ETF given the symbol
    """
    if not symbol:
        return jsonify({"error": "Symbol parameter is required"}), 400

    price_data = get_price_history(symbol)
    # Return the data as JSON
    return jsonify(price_data)


@assets_bp.route("/<key_word>", methods=["GET"])
def get_assets_by_keyword(key_word:str = None):
    """
    Endpoint to get the list of assets based on a keyword
    """
    if not key_word:
        return jsonify({"error": "Keyword parameter is required"}), 400

    assets = get_assets(key_word)
    return jsonify(assets), 200