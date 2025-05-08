from flask import Blueprint, request, jsonify

from app.openai_client import generate_portfolio_summary_insights, generate_portfolio_top_insights
from app.services import get_latest_price


insights_bp = Blueprint('insights', __name__)

@insights_bp.route('/portfolio/summary', methods=['POST'])
def get_robo_portfolio_summary_insights():
    data = request.get_json()
    portfolioValue = data.get("value")
    gainOrLossPercentage = data.get("gain_or_loss_percentage")
    assets = data.get("assets", {})
    
    response = generate_portfolio_summary_insights(portfolioValue, gainOrLossPercentage, assets)
    return jsonify({"message": response}), 200




@insights_bp.route('/portfolio/top', methods=['POST'])
def get_robo_portfolio_top_insights():
    data = request.get_json()
    assets = data.get("assets", [])

    enriched_assets = []
    for asset in assets:
        symbol = asset.get("symbol")
        current_price = get_latest_price(symbol)
        avg_price = asset.get("avgBuyPrice", 0)
        gain_pct = ((current_price - avg_price) / avg_price * 100) if avg_price > 0 else 0.0
        enriched_assets.append({
            "name": asset.get("name"),
            "sharesOwned": asset.get("sharesOwned", 0),
            "avgBuyPrice": avg_price,
            "currentPrice": current_price,
            "gainPercentage": gain_pct
        })

    sorted_assets = sorted(enriched_assets, key=lambda x: x["gainPercentage"], reverse=True)
    top_3 = sorted_assets[:3]
    bottom_3 = sorted_assets[-3:] if len(sorted_assets) > 3 else sorted_assets[::-1]

    for asset in enriched_assets:
        asset["gainPercentage"] = round(asset["gainPercentage"], 2)

    response = generate_portfolio_top_insights(
        enriched_assets, top_3, bottom_3
    )

    return jsonify({ "message": response}), 200