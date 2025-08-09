import csv
from datetime import datetime
from custom_types.Transaction import Transaction
from utils.load_save_data import transactions_observable
from utils.csv_definitions import ColumnType, Role, ColumnTypeParsers
import uuid
import re

def normalize(s):
    return re.sub(r'\s+', ' ', s.strip())

def loose_match_descriptions(a, b):
    a_norm = normalize(a)
    b_norm = normalize(b)
    return (
        a_norm == b_norm or
        a_norm in b_norm or
        b_norm in a_norm
    )

def get_column_data(value, column_type):
    parser = ColumnTypeParsers[column_type]
    return parser(value)

def parse_csv_to_transactions(file_path, csv_definition):
    transactions = []
    data = list(transactions_observable.get_data().values())
    with open(file_path, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        
        if csv_definition['hasHeaders']:
            next(csv_reader)

        col_with_type_flag = next(
            (col for col in csv_definition['columns'] if col['type'] == ColumnType.TYPE_FLAG),
            None
        )

        col_with_currency = next(
            (col for col in csv_definition['columns'] if col['type'] == ColumnType.CURRENCY_FLAG),
            None
        )

        col_with_second_amount = next(
            (col for col in csv_definition['columns'] if col['type'] == ColumnType.AMOUNT_SECOND),
            None
        )

        has_other_currency = col_with_currency is not None
        has_credit_debit_header = col_with_type_flag is not None

        # Iterate through the rows of the CSV (excluding header)
        for row in csv_reader:
            # Create a dictionary to store parsed transaction data
            transaction_data = {}
            for col_def in csv_definition['columns']:
                column_index = col_def['index']
                column_type = col_def['type']
                column_role = col_def['role']
                invert = col_def['invert'] if 'invert' in col_def else False
                value = row[column_index]

                if column_role == Role.NO_ROLE:
                    # Skip columns with no specific role
                    # Also skip if it has amount second, it is handled in regular amount iteration
                    continue

                transaction_data['uuid'] = str(uuid.uuid4())
                # Convert values based on the type defined in the csv_definition
                if column_role == Role.DATE:
                    try:
                        converted_value = get_column_data(value, column_type)
                        transaction_data['date'] = converted_value
                    except ValueError:
                        print(f"Error: Invalid date format in row: {row}")
                        continue
                elif column_role == Role.AMOUNT:
                    # Convert to float (assuming it's a currency)
                    try:
                        converted_value = get_column_data(value, column_type)
                        transaction_data['amount'] = converted_value
                    except ValueError:
                        print(f"Error: Invalid amount format in row: {row}")
                        continue

                    if has_credit_debit_header:
                        try:
                            creditDebitHeaderIndex = col_with_type_flag['index']
                            creditDebitHeaderValue = row[creditDebitHeaderIndex]
                            if str(creditDebitHeaderValue).lower() == 'credit':
                                transaction_data['amount'] = -transaction_data['amount']
                        except ValueError:
                            print(f"Error: Invalid credit/debit header format in row: {row}")
                            continue
                    
                    if has_other_currency:
                        currency_header_index = col_with_currency['index']
                        currency_header_value = row[currency_header_index]
                        # if the other currency column is provided and the amount exists, it will override the amount
                        if str(currency_header_value) == '$' and col_with_second_amount:
                            second_amount_value = row[col_with_second_amount['index']]
                            converted_value = get_column_data(second_amount_value, col_with_second_amount['type'])
                            transaction_data['amount'] = converted_value
                    
                    if invert:
                        transaction_data['amount'] = -transaction_data['amount']
                elif column_role == Role.DESCRIPTION:
                    converted_value = get_column_data(value, column_type)
                    transaction_data['description'] = converted_value

            # Ensure that 'date', 'amount', and 'description' are present for the transaction
            if 'date' in transaction_data and 'amount' in transaction_data and 'description' in transaction_data:
                # Check if the transaction already exists in the data list
                existing_transaction = None
                for existing in data:
                    if (existing.date == transaction_data['date'] and 
                        existing.amount == transaction_data['amount'] and
                        loose_match_descriptions(existing.description, transaction_data['description'])):
                        existing_transaction = existing
                        break

                if not existing_transaction:
                    # Create the Transaction object if it doesn't exist already
                    transaction = Transaction(tags=[], **transaction_data)
                    transactions.append(transaction)
                else:
                    print(f"Duplicate transaction found: {existing_transaction}")
    return transactions
