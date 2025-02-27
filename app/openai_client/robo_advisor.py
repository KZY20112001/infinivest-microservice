import json

from app.models import Portfolio, PortfolioResponse, Asset, AssetAllocationResponse
from .openai import format_message, get_response

def classify_transactions(transactions: str) -> str:
    """Classifies bank transactions into categories using OpenAI."""
    
    class_inst = """
    Categorize the bank transactions into 5 categories: essentials, discretionary, debt, savings, and miscellaneous. 
    These keywords below will be helpful to you. 

    essentials_keywords = ['grocery', 'utility', 'breakfast', 'lunch','dinner', 'rent', 'transport', 'electricity', 'ds', 'drink stall', 'water', 'canteen', 'delights', 'noodle', 'food']
    discretionary_keywords = ['edu', 'coursera', 'shopee', 'restaurant', 'shopping', 'entertainment', 'cinema', 'travel', 'tech'] 
    debt_keywords = ['loan', 'credit card', 'repayment', 'mortgage']
    savings_keywords = ['investment', 'savings', 'stock', 'deposit', 'fund']
    miscellaneous_keywords = ['misc', 'other']

    Input lines will be of this format:
    index description
    e.g., 0 DEBIT PURCHASE USD 15.00 23/08/24 xx-9691 AIRALO S

    Respond only with output lines of this format:
    index category
    """

    messages = [
        format_message("system", class_inst),
        format_message("user", transactions)
    ]
    return get_response(messages)


def generate_portfolio_split(expenditure_dict: dict, risk_tolerance_level:str) -> PortfolioResponse:
    class_inst = f"""
    You will be given the dictionary containing expenses spent in one month grouped into 4 categories: essentials, discretionary, debt, savings.
    You will also be given the user's risk tolerance level: low, medium, high.
    Use these information to suggest the percentage split in these categories (the recommended percentage may be zero):
    1. Large Cap Blend
    2. Small Cap Blend
    3. International Stocks
    4. Emerging Markets
    5. Intermediate Bonds
    6. International Bonds
    7. Cash


    Input line will be a dictionary containing the categories and the respective expenditure percentages followed by the risk tolerance level (low,medium or high):
    e.g. {{essentials': 40 , 'discretionary': 25, 'debt': 5, 'savings': 30}} low


    Respond with first part containing the recommended splits for the above categories. 
    And another part giving a short explanation (one paragraph) for why such split is recommended. 
    Ensure the total percentages for the categories sum up to 100. 
    Return in JSON format as shown in this example:
    e.g.
    {{ 
        "portfolio" : {{
              "large_cap_blend": 20,
              "small_cap_blend": 5,
              "international_stocks": 10,
              "emerging_markets": 5,
              "intermediate_bonds": 30,
              "international_bonds": 10,
              "cash": 20,
        }}, 
        "reason" : "This allocation prioritizes stability, income, and capital preservation while allowing for moderate growth"
    }}
    Note that the total percentages sum up to 20+5+10+2+30+10+15+3+5 = 100. 
    """ 
    input_message = str(expenditure_dict) + " " + risk_tolerance_level
    messages = [format_message("system", class_inst),
                    format_message("user", input_message)]
    res = get_response(messages)
    res_dict:dict = json.loads(res)
    portfolio_data = PortfolioResponse(
        portfolio=Portfolio(**res_dict["portfolio"]),
        reason=res_dict["reason"]
    )
    return portfolio_data



def generate_asset_allocation_split(category: str, total_percentage: str, invalid_list: list) -> AssetAllocationResponse: 
    excluded_symbols = ", ".join(invalid_list)
    exclusion_clause = f"You must not include the following assets in your answer: {excluded_symbols}." if excluded_symbols else ""
    class_inst = f"""
    You will be given a portfolio category from the following list and the total percentage to be allocated.
    Use that information to suggest a list of assets and the corresponding amount to be allocated to that asset.
    1. large_cap_blend
    2. small_cap_blend
    3. international_stocks
    4. emerging_markets
    5. intermeidate_bonds
    6. international_bonds


    Input will be a line containing the category (from the list above) followed by the total percentage.
    e.g. large_cap_blend 25

    {exclusion_clause}

    Return the recommended assets (their symbols) and their percentages in the JSON format as shown in this example:
    Ensure that the symbols are valid symbols, and the total percentages for the generated assets sum up to the total percentage provided.
    e.g.
    {{ 
        "SPY": 12,
        "VTI": 6,
        "GOOG": 3,
        "AAPL": 2,
        "MSFT": 2
    }}
    """
    input_message = category + " " + total_percentage
    messages = [format_message("system", class_inst),
                    format_message("user", input_message)]
    res = get_response(messages)

    assets_list = [Asset(symbol=k, percentage=v) for k, v in json.loads(res).items()]
    asset_allocation = AssetAllocationResponse(assets=assets_list)
    return asset_allocation