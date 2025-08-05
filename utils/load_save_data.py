import pickle
import os
from observables.unsaved_changes import unsaved_changes
from custom_types.transactionObservable import TransactionObservable

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

# Incase the module name gets changed
class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        print(module, name)
        if module == 'Transaction':
            module = 'custom_types.Transaction'
        return super().find_class(module, name)

def save_to_pickle_file():
    global file_path
    global transactions_observable
    """Save the data to a pickle file."""
    with open(file_path, 'wb') as f:
        pickle.dump(transactions_observable.get_expenses(), f)
        print("Data saved to pickle file successfully.")
        unsaved_changes.set_data(False)

file_path = './data.pkl'
data = load_pickle_file(file_path)

transactions_observable = TransactionObservable()
transactions_observable.set_data(data)