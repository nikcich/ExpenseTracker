import csv
from datetime import datetime
from Transaction import Transaction
from load_save_data import transactions_observable
from tags import tags


def parse_csv_to_transactions(file_path, csv_definition):
    transactions = []
    data = transactions_observable.get_data()
    with open(file_path, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        
        # Read the header (first row)
        headers = next(csv_reader)
        
        # Validate the headers against the csv_definition
        if headers != csv_definition['headers']:
            print("Error: CSV headers do not match the expected format.")
            return []

        # Iterate through the rows of the CSV (excluding header)
        for row in csv_reader:
            # Create a dictionary to store parsed transaction data
            transaction_data = {}
            for col_def in csv_definition['columns']:
                column_index = col_def['index']
                column_type = col_def['type']
                value = row[column_index]
                header = headers[column_index]
                isDateHeader = header == csv_definition['date_header']
                isAmountHeader = header == csv_definition['amount_header']
                isDescriptionHeader = header == csv_definition['description_header']

                # Convert values based on the type defined in the csv_definition
                if column_type == 'date' and isDateHeader:
                    # Convert date string to a proper date format
                    try:
                        transaction_data['date'] = datetime.strptime(value, "%m/%d/%Y").strftime("%m/%d/%Y")
                    except ValueError:
                        print(f"Error: Invalid date format in row: {row}")
                        continue
                elif column_type == 'float' and isAmountHeader:
                    # Convert to float (assuming it's a currency)
                    try:
                        transaction_data['amount'] = float(value.replace('$', '').replace(',', '').strip())
                    except ValueError:
                        print(f"Error: Invalid amount format in row: {row}")
                        continue
                elif column_type == 'string' and isDescriptionHeader:
                    transaction_data['description'] = value

            # Ensure that 'date', 'amount', and 'description' are present for the transaction
            if 'date' in transaction_data and 'amount' in transaction_data and 'description' in transaction_data:
                # Check if the transaction already exists in the data list
                existing_transaction = None
                for existing in data:
                    if (existing.date == transaction_data['date'] and 
                        existing.amount == transaction_data['amount'] and
                        existing.description == transaction_data['description']):
                        existing_transaction = existing
                        break

                if not existing_transaction:
                    # Create the Transaction object if it doesn't exist already
                    transaction = Transaction(tags=[], **transaction_data)
                    transactions.append(transaction)
                else:
                    print(f"Duplicate transaction found: {existing_transaction}")
    
    return transactions
