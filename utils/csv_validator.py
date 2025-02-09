# csv_validator.py
import csv
from datetime import datetime

# Function to validate data types (this can be expanded to include more types)
def validate_data(value, column_type):
    if column_type == 'date':
        try:
            # Attempt to convert the value to a valid date format
            datetime.strptime(value, "%m/%d/%Y")
        except ValueError:
            return False
    elif column_type == 'float':
        try:
            # Remove currency symbols and commas before checking if it's a valid float
            value = value.replace('$', '').replace(',', '').strip()
            float(value)
        except ValueError:
            return False
    elif column_type == 'string':
        return True
    return True

# Generic CSV Validation function
def validate_csv(file_path, csv_definition):
    """
    Validates a CSV file against a given definition.

    Args:
    - file_path: The path to the CSV file.
    - csv_definition: A dictionary with 'headers' and 'columns' validation info.
      Example:
      {
        'headers': ['Header1', 'Header2', ...],
        'columns': [
            {'type': 'string', 'index': 0},
            {'type': 'date', 'index': 1},
            {'type': 'float', 'index': 2}
        ]
      }

    Returns:
    - True if the file matches the format, False otherwise.
    """
    # Open the CSV file
    try:
        with open(file_path, mode='r', newline='') as file:
            csv_reader = csv.reader(file)
            
            # Read the header (first row)
            headers = next(csv_reader)
            
            # Validate header
            if headers != csv_definition['headers']:
                print("Error: Headers do not match the expected format.")
                return False
            
            # Validate each row
            row_number = 1  # Start counting rows from 1 (skipping the header)
            for row in csv_reader:
                row_number += 1
                # Check if the row has the correct number of columns
                if len(row) != len(csv_definition['headers']):
                    print(f"Error: Row {row_number} has an incorrect number of columns.")
                    return False
                
                # Validate each column based on the definition
                for col_def in csv_definition['columns']:
                    column_index = col_def['index']
                    column_type = col_def['type']
                    if not validate_data(row[column_index], column_type):
                        print(f"Error: Row {row_number} has invalid data in column {column_index + 1} ({headers[column_index]}).")
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
