from flask import current_app
import json
from openai import OpenAI

from app.models.portfolio import Portfolio, PortfolioResponse


def format_message(role: str, content: str) -> dict:
    """Formats a message for OpenAI API request."""
    return {"role": role, "content": content}


def get_response(messages: list) -> str:
    """Calls OpenAI API to get a response based on the provided messages."""
    
    client = OpenAI(
    api_key= current_app.config['OPENAI_API_KEY'],
    )
    completion = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages,
    ) 
    return completion.choices[0].message.content



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
    8. Commodities
    9. REITs

    Input line will be a dictionary containing the categories and the respective expenditure percentages followed by the risk tolerance level (low,medium or high):
    e.g. {{essentials': 40 , 'discretionary': 25, 'debt': 5, 'savings': 30}} low


    Respond with first part containing the recommended splits for the above categories. 
    And another part giving a short explanation (one paragraph) for why such split is recommended based on the given expenditure and risk tolerance. 
    Return in JSON format as shown in this example:
    e.g.
    {{ 
        "portfolio" : {{
              "large_cap_blend": 20,
              "small_cap_blend": 5,
              "international_stocks": 10,
              "emerging_markets": 2,
              "intermediate_bonds": 30,
              "international_bonds": 10,
              "cash": 15,
              "commodities": 3,
              "reits": 5
        }}, 
        "reason" : "This allocation prioritizes stability, income, and capital preservation while allowing for moderate growth"
    }}
    """ 
    print(expenditure_dict)
    input_message = str(expenditure_dict) + " " + risk_tolerance_level
    messages = [format_message("system", class_inst),
                    format_message("user", input_message)]
    res = get_response(messages)
    res_dict = json.loads(res)
    portfolio_data = PortfolioResponse(
        portfolio=Portfolio(**res_dict["portfolio"]),
        reason=res_dict["reason"]
    )
    return portfolio_data

