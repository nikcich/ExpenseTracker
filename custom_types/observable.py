import inspect

class Observable:
    def __init__(self):
        self._observers = []  
        self._data = None

    def add_observer(self, observer):
        """Add an observer function to the list of observers."""
        self._observers.append(observer)

    def remove_observer(self, observer):
        """Remove an observer function from the list."""
        self._observers.remove(observer)

    def set_data(self, data):
        """Set the data and notify all observers."""
        self._data = data
        self._notify_observers()

    def get_data(self):
        """Return the current data."""
        return self._data

    def _notify_observers(self):
        """Notify all observers when the data changes."""
        for observer in self._observers:
            if self._has_argument(observer):
                observer(self._data)  # Call with data argument
            else:
                observer()  # Call without argument
    def _has_argument(self, observer):
        """Check if the observer function accepts arguments."""
        # Inspect the observer's signature to see if it requires parameters
        signature = inspect.signature(observer)
        # If the observer function has parameters, return True (expects data)
        return len(signature.parameters) > 0