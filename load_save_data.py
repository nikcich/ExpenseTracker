import pickle
import os
import inspect
from observable import Observable
from unsaved_changes import unsaved_changes

def load_pickle_file(file_path):
    """Load the pickle file if it exists."""
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
            print("Pickle file loaded successfully.")
            return data
    else:
        print("Pickle file does not exist.")
        return []

def save_to_pickle_file():
    global file_path
    global transactions_observable
    """Save the data to a pickle file."""
    with open(file_path, 'wb') as f:
        pickle.dump(transactions_observable.get_data(), f)
        print("Data saved to pickle file successfully.")
        unsaved_changes.set_data(False)

file_path = 'data.pkl'
data = load_pickle_file(file_path)

transactions_observable = Observable()
transactions_observable.set_data(data)