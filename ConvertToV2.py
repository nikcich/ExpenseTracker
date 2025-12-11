import os
import sys
import pickle
import csv

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

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <pickle_file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    data = load_pickle_file(file_path)
    print("Contents of the pickle file:")
    print(data)
    csv_data = []
    for transaction_id, transaction in data.items():
        tags = [tag['tag_name'] for tag in transaction.tags]
        csv_data.append([tags[0] if tags else '', transaction.date, transaction.description, str(transaction.amount)])

    filename = 'output.csv'
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Tags', 'Date', 'Description', 'Amount'])
        writer.writerows(csv_data)

if __name__ == "__main__":
    main()
