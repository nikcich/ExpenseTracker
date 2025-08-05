import os
import sys
import pickle
from custom_types.Transaction import Transaction
import re

def normalize(s):
    return re.sub(r'\s+', ' ', s.strip())

# Optional: define CustomUnpickler if you're using it
class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Modify this if needed for custom classes/modules
        return super().find_class(module, name)

def load_pickle_file(file_path):
    """Load the pickle file if it exists."""
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            data = CustomUnpickler(f).load()
            print("Pickle file loaded successfully.")
            return data
    else:
        print("Pickle file does not exist.")
        return []

def convert_to_new_transaction(old_tx):
    return Transaction(
        amount=old_tx.amount,
        date=old_tx.date,
        description=normalize(old_tx.description),
        tags=getattr(old_tx, 'tags', [])
    )

def save_to_pickle_file(data):
    """Save the data to a pickle file."""
    with open("converted_save_data.pkl", 'wb') as f:
        pickle.dump(data, f)
        print("Data saved to pickle file successfully.")

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <pickle_file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    data = load_pickle_file(file_path)
    print("Contents of the pickle file:")
    converted = [convert_to_new_transaction(tx) for tx in data]
    print(converted)
    save_to_pickle_file(converted)

    

if __name__ == "__main__":
    main()
