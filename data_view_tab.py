from load_save_data import transactions_observable  # Assuming 'data' is the list of transactions
from transaction_table import TransactionTable  # Assuming the TransactionTable class is in 'transaction_table.py'
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget, QMainWindow
from load_save_data import transactions_observable  # Assuming 'transactions_observable' is the observable object

class DataViewTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.transaction_count_label = QLabel(self)
        self.transaction_table = None

        self.refresh()

        transactions_observable.add_observer(self.refresh)

    def refresh(self):
        sliderPos = self.transaction_table.table_widget.verticalScrollBar().sliderPosition() if self.transaction_table is not None else 0

        """Refresh the content of this tab."""
        # Update transaction count label
        transactions = transactions_observable.get_data()
        self.transaction_count_label.setText(f"Number of Transactions: {len(transactions)}")

        # Remove the placeholder label
        if self.transaction_table:
            self.layout.removeWidget(self.transaction_table)
            self.transaction_table.deleteLater()

        # Create and add the updated transaction table
        self.transaction_table = TransactionTable(self, transactions, sliderPos)
        self.layout.addWidget(self.transaction_table)
        self.layout.addWidget(self.transaction_count_label)
