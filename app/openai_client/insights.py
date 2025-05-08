from .openai import get_response, format_message

def generate_portfolio_summary_insights(portfolioValue: float, gainOrLossPercentage: float, assets: list[dict]) -> str:
    system_message = """
        You are a helpful financial assistant. Your job is to review a user's portfolio and give a concise, insightful summary.

        Use the portfolio's total value, gain/loss percentage, and the list of assets (with shares owned and average buy price) to identify trends or areas worth highlighting.

        Your tone should be friendly, clear, and professional. Do not suggest specific investments—focus on summarizing what's already there.
            """

    asset_lines = []
    for asset in assets:
        line = f"- {asset['name']}: {asset['sharesOwned']} shares at avg. buy price ${asset['avgBuyPrice']:.2f}"
        asset_lines.append(line)
    asset_text = "\n".join(asset_lines) if asset_lines else "No assets provided."

    user_message = f"""
        Here is my Robo Portfolio Summary:

        - Total Value: ${portfolioValue:,.2f}
        - Gain/Loss Percentage: {gainOrLossPercentage:.2f}%

        Assets:
        {asset_text}

        Please provide a paragraph showing your insights for this portfolio performance and future potential.
        """

    messages = [
        format_message("system", system_message.strip()),
        format_message("user", user_message.strip())
    ]

    return get_response(messages)

def generate_portfolio_top_insights(
    assets: list[dict],
    top_3: list[dict],
    bottom_3: list[dict]
) -> str:

    system_message = """
        You are a helpful financial assistant. Review the user's portfolio and provide a concise, insightful summary.

        Include:
        - Top 3 best-performing assets.
        - Top 3 worst-performing assets.
        - Notable patterns (e.g., sector concentration, significant gains or losses).

        Maintain a clear, friendly, and professional tone. Avoid suggesting new investments.
    """

    # Format asset details
    def format_asset_details(asset_list):
        return "\n".join(
            f"- {asset['name']}: {asset['sharesOwned']} shares at avg. buy price ${asset['avgBuyPrice']:.2f}, "
            f"current price ${asset['currentPrice']:.2f}, gain {asset['gainPercentage']:.2f}%"
            for asset in asset_list
        )

    all_assets_text = format_asset_details(assets)
    top_3_text = format_asset_details(top_3)
    bottom_3_text = format_asset_details(bottom_3)

    user_message = f"""
        Here are my Portfolio assets:


        Assets:
        {all_assets_text}

        Top 3 Performing Assets:
        {top_3_text}

        Bottom 3 Performing Assets:
        {bottom_3_text}

        Return the top 3 and bottom 3 performing assets (with their names) and also provide some insights on other assets and point out trends. 
        Return as normal paragraph (no bold etc)
    """

    messages = [
        format_message("system", system_message.strip()),
        format_message("user", user_message.strip())
    ]

    return get_response(messages)
