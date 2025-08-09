# csv_validator.py
import csv
from utils.csv_parser_functions import ColumnTypeParsers
from utils.csv_definitions import Role
from utils.csv_parser_functions import get_column_data


# Function to validate data types (this can be expanded to include more types)
def validate_data(value, column_type):
    try:
        parser = ColumnTypeParsers[column_type]
        parser(value)
        return True
    except ValueError:
        return False

def validate_metadata(meta_def, row, value):
        try:
            meta_cols = meta_def['columns']
            handler = meta_def['handler']
            handler(meta_cols, row, value)
            return True
        except ValueError:
            return False

# Generic CSV Validation function
def validate_csv(file_path, csv_definition):
    # Open the CSV file
    try:
        with open(file_path, mode='r', newline='') as file:
            csv_reader = csv.reader(file)

            # Validate each row
            if csv_definition['hasHeaders']:
                next(csv_reader)  # Skip header row
            
            row_number = 0  # Start counting rows from 1 (skipping the header)
            for row in csv_reader:
                row_number += 1
                # Check if the row has the correct number of columns
                if len(row) < len(csv_definition['columns']):
                    # print(f"Error: Row {row_number} has an incorrect number of columns.")
                    return False
                
                columns = csv_definition['columns']
                meta = csv_definition['metadata']

                # Validate each column based on the definition
                for role in Role:
                    col_def = columns[role]
                    meta_def = meta[role]
                    if not col_def:
                        return False
                    column_index = col_def['index']
                    column_type = col_def['type']
                    if not validate_data(row[column_index], column_type):
                        return False
                    
                    if len(meta_def) > 0:
                        for meta_item in meta_def:
                            value = get_column_data(row[column_index], column_type)
                            if not validate_metadata(meta_item, row, value):
                                return False
                
            return True
            
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
