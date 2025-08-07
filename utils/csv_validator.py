# csv_validator.py
import csv
from datetime import datetime
from utils.csv_definitions import ColumnTypeParsers

# Function to validate data types (this can be expanded to include more types)
def validate_data(value, column_type):
    try:
        parser = ColumnTypeParsers[column_type]
        parser(value)
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
                    print(f"Error: Row {row_number} has an incorrect number of columns.")
                    return False
                
                # Validate each column based on the definition
                for col_def in csv_definition['columns']:
                    column_index = col_def['index']
                    column_type = col_def['type']
                    if not validate_data(row[column_index], column_type):
                        print(f"Error: Row {row_number} has invalid data in column {col_def}.")
                        print(row[column_index], column_type)
                        return False
            
            print("CSV file is valid.")
            return True
            
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
