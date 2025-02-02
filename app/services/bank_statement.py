from werkzeug.datastructures import FileStorage
import pandas as pd

from app.models.portfolio import PortfolioResponse
from app.utils.bank_statement_parsers import parse_OCBC_bank_statement, parse_SC_bank_statement
from app.utils.openai_client import classify_transactions, generate_portfolio_split 

def generate_portfolio(bank_statement: FileStorage, bank_name: str, risk_tolerance_level:str="medium") -> PortfolioResponse:
    """
    Takes in a bank statement (pdf) and the corresponding bank name. 
    Returns a recommended portfolio style based on the bank statement. 
    """
    
    transactions: list = []
    match bank_name: 
        case "ocbc": 
            transactions = parse_OCBC_bank_statement(bank_statement)
        case "sc": 
            transactions = parse_SC_bank_statement(bank_statement)
            
    # create a dataframe from the transactions
    df = create_dataframe(transactions)
    
    # add categorization for each expense
    df = add_category(df)
    
    expenses_dict = calc_expenses(df)
    
    return generate_portfolio_split(expenses_dict, risk_tolerance_level)
    

def create_dataframe(transactions: list) -> pd.DataFrame: 
    """
    Takes in a list of transactions and return a dataframe after filtering out deposit-related transactions. 
    """
    df = pd.DataFrame(transactions) 
    df = df.drop(df[df.type == 'deposit'].index) # drop deposit  
    return df.drop(columns=['type']).reset_index(drop=True)  # only return expenses

def add_category(df: pd.DataFrame) -> pd.DataFrame: 
    """
    Use OpenAI LLM to classify transactions in the dataframe into 5 categories: essentials, discretionary, debt, savings, and miscellaneous. 
    Appends a new column called "category" for each transactions. 
    Returns the updated df 
    """
    max_index = len(df)
    descriptions = df['description']
    category_dict = {}
    batch = []
    
    for i, desc in enumerate(descriptions):
        batch.append(f"{i} {desc}") 
        if len(batch) == 200 or i == len(df) - 1:  
            categories = classify_transactions("\n".join(batch)).split('\n')  
            for category in categories: 
                array = category.strip().split(' ')
                if len(array) == 2 and array[0].isdigit(): 
                    idx = int(array[0])
                    if 0 <= idx < max_index:
                        category_dict[array[0]] = array[1]
            batch = [] 

    df['category'] = df.index.map(lambda x: category_dict.get(str(x), 'miscellaneous'))
    return df



def calc_expenses(df: pd.DataFrame) -> dict: 
    """
    Calculate the expenses for each category as a percentage (ignoring "miscellaneous" category)
    Returns a dict containing percentages
    """
    categories = ['essentials', 'discretionary', 'debt', 'savings']
    expenses_dict = {category: 0 for category in categories}
    total_amount = df[df['category'] != 'miscellaneous']['amount'].sum()
    
    # Update percentages for each category except 'miscellaneous'
    for _, row in df.iterrows():
        if row['category'] != 'miscellaneous':
            expenses_dict[row['category']] += (row['amount'] / total_amount) * 100
    
    return expenses_dict
    
