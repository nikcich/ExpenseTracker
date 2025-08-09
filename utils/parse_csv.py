import csv
from datetime import datetime
from custom_types.Transaction import Transaction
from utils.load_save_data import transactions_observable
from utils.csv_definitions import Role
from utils.csv_parser_functions import get_column_data

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

def parse_csv_to_transactions(file_path, csv_definition):
    transactions = []
    data = list(transactions_observable.get_data().values())
    with open(file_path, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        
        if csv_definition['hasHeaders']:
            next(csv_reader)

        columns = csv_definition['columns']
        meta = csv_definition['metadata']

        # Iterate through the rows of the CSV (excluding header)
        for row in csv_reader:
            # Create a dictionary to store parsed transaction data
            transaction_data = {}
        
            for role in Role:
                col_def = columns[role]
                meta_def = meta[role]
                column_index = col_def['index']
                column_type = col_def['type']
                column_role = role
                invert = col_def['invert'] if 'invert' in col_def else False
                value = row[column_index]
                transaction_data['uuid'] = str(uuid.uuid4())

                try:
                    converted_value = get_column_data(value, column_type)
                except ValueError:
                    print(f"Error: Invalid value '{value}' for column type '{column_type}' in row: {row}")
                    continue

                if meta_def is not None and len(meta_def) > 0:   
                    for meta_item in meta_def:
                        meta_cols = meta_item['columns']
                        handler = meta_item['handler']
                        converted_value = handler(meta_cols, row, converted_value)

                if invert:
                        converted_value = -converted_value

                if column_role == Role.DATE:
                    transaction_data['date'] = converted_value
                elif column_role == Role.DESCRIPTION:
                    transaction_data['description'] = converted_value
                elif column_role == Role.AMOUNT:
                    transaction_data['amount'] = converted_value

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