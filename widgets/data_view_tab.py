from utils.load_save_data import transactions_observable  # Assuming 'data' is the list of transactions
from widgets.transaction_table import TransactionTable  # Assuming the TransactionTable class is in 'transaction_table.py'
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

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
        sort_column = self.transaction_table.table_widget.horizontalHeader().sortIndicatorSection() if self.transaction_table is not None else -1
        sort_order = self.transaction_table.table_widget.horizontalHeader().sortIndicatorOrder() if self.transaction_table is not None else Qt.AscendingOrder

        # Save the current column widths
        column_widths = []
        if self.transaction_table is not None:
            column_widths = [self.transaction_table.table_widget.columnWidth(i) for i in range(self.transaction_table.table_widget.columnCount())]

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

        # Restore the previous sort order and column
        if sort_column != -1:
            self.transaction_table.table_widget.sortItems(sort_column, sort_order)
        self.transaction_table.table_widget.verticalScrollBar().setSliderPosition(sliderPos)

        # Restore the previous column widths
        if column_widths:
            for i, width in enumerate(column_widths):
                self.transaction_table.table_widget.setColumnWidth(i, width)