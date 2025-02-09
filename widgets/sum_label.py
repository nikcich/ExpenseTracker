from PyQt5 import QtWidgets, QtCore
from utils.load_save_data import transactions_observable
from observables.visible_tags import visibleTags
from PyQt5.QtCore import QDate

class TotalAmountLabel(QtWidgets.QWidget):
    def __init__(self, start_date, end_date):
        super().__init__()

        # Create the QLabel to display the total amount
        self.data_sum_label = QtWidgets.QLabel("", self)
        self.data_sum_label.setAlignment(QtCore.Qt.AlignLeft)
        self.data_sum_label.setStyleSheet("font-size: 16px; color: white; font-weight: bold;")

        # Set up layout
        vlayout = QtWidgets.QVBoxLayout(self)
        vlayout.addWidget(self.data_sum_label)

        # Store the start and end date
        self.start_date = start_date
        self.end_date = end_date

        # Initialize the sum label
        self.update_total_amount()

        # Add observer for transactions to update the label when data changes
        transactions_observable.add_observer(self.update_total_amount)
        visibleTags.add_observer(self.update_total_amount)
        start_date.add_observer(self.update_total_amount)
        end_date.add_observer(self.update_total_amount)

    def update_total_amount(self):
        # Get the list of transactions
        transactions = transactions_observable.get_data()

        # Get the list of visible tags
        visible_tags = visibleTags.get_data()

        # Get the start and end dates from the input
        start_date = self.start_date.get_data()
        end_date = self.end_date.get_data()

        # Initialize the total sum
        total_sum = 0

        # Iterate through the transactions and sum those with a visible tag within the date range
        for transaction in transactions:
            # Convert the transaction date from string "MM/DD/YYYY" to QDate
            transaction_date = QDate.fromString(transaction.date, 'MM/dd/yyyy')

            # Filter transactions within the date range
            if start_date <= transaction_date <= end_date:
                # Check each tag for the transaction
                for tag in transaction.tags:
                    tag_name = tag['tag_name']
                    # Check if any tag is visible
                    if tag_name in visible_tags:
                        total_sum += transaction.amount  # Add the absolute value to the sum (positive amount)

        # Update the QLabel text with the total sum
        self.data_sum_label.setText(f"Total over period: ${total_sum:,.2f}")
