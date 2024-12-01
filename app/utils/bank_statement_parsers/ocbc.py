import re

from werkzeug.datastructures import FileStorage
import pymupdf

def is_indented(line:str) -> bool:
    return len(line) - len(line.lstrip()) >= 8

def parse_OCBC_bank_statement(bank_statement: FileStorage) -> list: 
    transactions = []
    bank_statement_bytes = bank_statement.read()
    
    with pymupdf.open(stream=bank_statement_bytes, filetype='pdf') as doc:
        for pageNo in range(len(doc)):
            current_transaction: dict = {}
                
            if pageNo == 1 or pageNo == len(doc)-1:
                continue
            
            page:str = doc[pageNo].get_text()
            lines = page.split('\n')
            #skip first lines till transactions lines are reached i.e skip till "Account No."
            i = 0
            while i < len(lines):
                curLine = lines[i]
                if pageNo == 0 and i == 0 and curLine != "OCBC Bank": 
                    print("Current PDF is not OCBC Bank Statement")
                    return
                words = lines[i].split(' ')
                i+=1
                if (len(words) >= 2 and words[0] == "Account" and words[1] == "No."): 
                    i+=1
                    break

            if pageNo == 0: 
                cur_balance = float(lines[i].strip().replace(",", ""))
                i+=2
            
            #get transactions
            while i < len(lines): 
                line = lines[i]
                i+=1
                
                if not line.strip():
                    continue
                
                # if no more transactions are left, break the loop in the second final page 
                if pageNo == len(doc) - 2 and line == 'BALANCE C/F': 
                    break
                
                if re.match(r'\d{2} \w{3}', line.strip()):
                        # If there's an ongoing transaction and we encounter a new date, complete the transaction
                        if 'posting_date' in current_transaction and 'transaction_date' in current_transaction:
                            # Determine if it's a deposit or withdrawal based on balance change
                            if current_transaction['balance'] > cur_balance:
                                current_transaction['type'] = 'deposit'
                            else:
                                current_transaction['type'] = 'withdrawal'

                            # Store the transaction
                            transactions.append(current_transaction)

                            # Update the previous balance
                            cur_balance = current_transaction['balance']
                            current_transaction = {}

                        # If there is already a transaction date in progress, this line is the "posting date"
                        if 'transaction_date' in current_transaction:
                            current_transaction['posting_date'] = line.strip()
                        else:
                            # Start a new transaction with the transaction date
                            current_transaction = {'transaction_date': line.strip()}

                    # Check for transaction amount (indented number)
                elif line.strip().replace(',', '').replace('.', '').isdigit() and is_indented(line):
                    amount = float(line.strip().replace(',', ''))
                    if 'amount' not in current_transaction:
                        current_transaction['amount'] = amount
                    else:
                        current_transaction['balance'] = amount

                # Append description details
                else:

                    if 'description' in current_transaction:
                        current_transaction['description'] += ' ' + line.strip()
                    else:
                        current_transaction['description'] = line.strip()

            # Handle the last transaction after the loop
            if current_transaction and 'balance' in current_transaction:
                if current_transaction['balance'] > cur_balance:
                    current_transaction['type'] = 'deposit'
                else:
                    current_transaction['type'] = 'withdrawal'
                transactions.append(current_transaction)
               
    transactions = [
        {key: value for key, value in transaction.items() if key not in ['posting_date', 'transaction_date']}
        for transaction in transactions
    ]
    return transactions