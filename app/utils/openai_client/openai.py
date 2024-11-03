from flask import current_app
from openai import OpenAI


client = OpenAI(
    api_key= current_app.config['OPENAI_API_KEY'],
)

def format_message(role: str, content: str) -> dict:
    """Formats a message for OpenAI API request."""
    return {"role": role, "content": content}


def get_response(messages: list) -> str:
    """Calls OpenAI API to get a response based on the provided messages."""
    
    completion = client.ChatCompletion.create(
        model='gpt-4o-mini',
        messages=messages,
    )
    return completion.choices[0].message.content


def classify_transactions(transactions: str) -> str:
    """Classifies bank transactions into categories using OpenAI."""
    
    class_inst = """
    Categorize the bank transactions into 5 categories: essentials, discretionary, debt, savings, and miscellaneous. 
    These keywords below will be helpful to you. 

    essentials_keywords = ['grocery', 'utility', 'rent', 'transport', 'electricity', 'ds', 'drink stall', 'water', 'canteen', 'delights', 'noodle', 'food']
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


def classify_portfolio(expenditure_dict: dict) -> str:
    """Suggests a stock portfolio based on expenditure categories using OpenAI."""
    class_inst = """
    You will be given the dictionary containing expenses spent in one month grouped into 4 categories: essentials, discretionary, debt, savings.
    Use that information to suggest the user's stock portfolio from these 19 categories:
    1. 7Twelve Portfolio
    2. All Seasons Portfolio
    3. Classic 60-40 Portfolio
    4. Coffeehouse Portfolio
    5. Core Four Portfolio
    6. Global Market Portfolio
    7. Golden Butterfly Portfolio
    8. Ideal Index Portfolio
    9. Ivy Portfolio
    10. Larry Portfolio
    11. No-Brainer Portfolio
    12. Permanent Portfolio
    13. Pinwheel Portfolio
    14. Sandwich Portfolio
    15. Swensen Portfolio
    16. Three-Fund Portfolio
    17. Total Stock Market Portfolio
    18. Ultimate Buy and Hold Portfolio
    19. Weird Portfolio

    Input line will be a dictionary containing the categories and the respective expenditure percentages:
    e.g., {'essentials': 40, 'discretionary': 25, 'debt': 5, 'savings': 30}

    Respond only with one line containing the category:
    e.g., All Seasons Portfolio
    """

    messages = [
        format_message("system", class_inst),
        format_message("user", str(expenditure_dict))
    ]
    return get_response(messages)
