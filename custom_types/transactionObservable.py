from custom_types.observable import Observable

class TransactionObservable:
    def __init__(self):
        self._observable = Observable()

    def add_observer(self, observer):
        self._observable.add_observer(observer)

    def remove_observer(self, observer):
        self._observable.remove_observer(observer)

    def _notify_observers(self):
        self._observable._notify_observers()

    def set_data(self, data):
        self._observable.set_data(data)

    def get_data(self):
        return self._observable.get_data()

    def get_income(self):
        """Return transactions that have an 'Income' tag."""
        data = self.get_data() or []
        return [
            t for t in data
            if any(tag.get('tag_name') == 'Income' for tag in (t.tags or []))
        ]

    def get_expenses(self):
        """Return transactions that do not have an 'Income' tag."""
        data = self.get_data() or []
        return [
            t for t in data
            if not any(tag.get('tag_name') == 'Income' for tag in (t.tags or []))
        ]
