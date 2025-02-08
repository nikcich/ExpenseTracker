from PyQt5.QtWidgets import QAbstractItemView, QListWidgetItem, QCheckBox, QListWidget, QDialog, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHeaderView, QLabel, QHBoxLayout, QSizePolicy, QPushButton
from PyQt5.QtCore import Qt, QDate
from tags import tags
from load_save_data import transactions_observable
from unsaved_changes import unsaved_changes

class CustomTableWidgetItem(QTableWidgetItem):
    def __init__(self, column, text):
        super().__init__(text)
        self.column = column
    def __lt__(self, other):
        column = self.column
        if column == 1:  # Date column
            return QDate.fromString(self.text(), 'yyyy-MM-dd') < QDate.fromString(other.text(), 'yyyy-MM-dd')
        elif column == 3:  # Amount column
            return float(self.text().replace('$', '').replace(',', '')) < float(other.text().replace('$', '').replace(',', ''))
        else:
            return super().__lt__(other)

class TransactionTable(QWidget):
    def __init__(self, parent, transactions, sliderPos):
        super().__init__(parent)
        
        # Create the table widget
        self.table_widget = QTableWidget(self)
        
        # Set the number of columns (Tags, Date, Description, Amount)
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Tags", "Date", "Description", "Amount"])
        
        # Store transactions and their original indices
        self.transactions = transactions
        self.sliderPos = sliderPos

        # Set up the table
        self.refresh()

        # Enable sorting on the columns
        self.table_widget.setSortingEnabled(True)  # Enable the built-in sorting

        # Allow columns to stretch and take up the full width
        header = self.table_widget.horizontalHeader()
        self.table_widget.resizeColumnsToContents()
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setStretchLastSection(True)

        # Set the size policy to expand horizontally
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add the table widget to the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.table_widget)
        self.setLayout(layout)

        # Connect the double-click event to a method for handling tag selection
        self.table_widget.cellDoubleClicked.connect(self.on_cell_double_clicked)

    def refresh(self):
        """Refresh the content of the table"""
        # Set the number of rows to match the transactions
        self.table_widget.setRowCount(len(self.transactions))
        self.table_widget.verticalScrollBar().setMaximum(len(self.transactions))
        self.table_widget.verticalScrollBar().setValue(self.sliderPos)
        
        for row, transaction in enumerate(self.transactions):
            # Format the amount as currency but keep the numeric value for sorting
            formatted_amount = f"${transaction.amount:,.2f}"

            # Convert transaction.date to QDate object
            transaction_date = QDate.fromString(transaction.date, 'MM/dd/yyyy')

            self.table_widget.setItem(row, 1, CustomTableWidgetItem(1, transaction_date.toString('yyyy-MM-dd')))  # Date column
            self.table_widget.setItem(row, 2, CustomTableWidgetItem(2, transaction.description))  # Description column
            self.table_widget.setItem(row, 3, CustomTableWidgetItem(3, formatted_amount))  # Amount column

            # Create a widget to hold the tags (pills)
            tag_widget = QWidget() 
            tag_layout = QHBoxLayout(tag_widget) 
            tag_layout.setContentsMargins(3, 0, 3, 0) 
            tag_layout.setSpacing(5)
            tag_layout.setAlignment(Qt.AlignLeft) 
            tag_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

            for tag in transaction.tags:
                color = tag['color']  # Hex color code
                name = tag['tag_name'] 
                
                pill = QPushButton(name)
                pill.setStyleSheet(f"""
                    background-color: {color};
                    border-radius: 10px;
                    color: white;
                    height: 20px;
                    padding-left: 8px;
                    padding-right: 8px;
                    text-align: center;
                    white-space: nowrap;
                """)
                
                pill.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
                pill.setAttribute(Qt.WA_TransparentForMouseEvents, True)
                tag_layout.addWidget(pill) 

            # Set the custom widget (with tags) in the first column
            self.table_widget.setCellWidget(row, 0, tag_widget)  # Tags column with pills

        # Restore the scroll position after refreshing
        self.table_widget.verticalScrollBar().setValue(self.sliderPos)

    def update_table(self, transactions):
        """Update the table with a new list of transactions"""
        self.transactions = transactions
        self.refresh()


    def match_transaction(self, date, desc, amount):
        if date and desc and amount:
            matching_transactions = [
                trans for trans in self.transactions 
                if (QDate.fromString(trans.date, 'MM/dd/yyyy').toString('yyyy-MM-dd') == date and 
                    trans.description == desc and 
                    f"${trans.amount:,.2f}" == amount)
            ]
        
        if matching_transactions:
            return matching_transactions[0]  # Take first match
        else:
            return None

    def on_cell_double_clicked(self, row, column):
        """Handle cell double-click events and open a popup for tag selection."""
        if column == 0:  # If the Tags column (index 0) is double-clicked
            # Retrieve the QTableWidgetItem for the clicked cell
            item = self.table_widget.cellWidget(row, column)
            date = self.table_widget.item(row, 1)
            description = self.table_widget.item(row, 2)
            amount = self.table_widget.item(row, 3)

            # Ensure the item is not None and get the original transaction
            if item:
                transaction = self.match_transaction(date.text(), description.text(), amount.text())
                if transaction:
                    dialog = QDialog(self)
                    dialog.setWindowTitle("Select Tags")  
                    dialog.setFixedSize(300, 300) 

                    layout = QVBoxLayout(dialog)

                    label = QLabel("Select the tags for this transaction:")
                    layout.addWidget(label)

                    list_widget = QListWidget(dialog)
                    
                    # Create a QListWidget for tags
                    for tag_key, tag_data in tags.items():
                        tag_name = tag_data['tag_name']

                        # Check if the tag already exists in the transaction
                        tag_exists = any(tag['tag_name'] == tag_name for tag in transaction.tags)

                        item = QListWidgetItem(tag_name)  # Create the item with the tag name
                        checkbox = QCheckBox(tag_name)  # Create the checkbox widget
                        checkbox.setChecked(tag_exists)  # Set checkbox state

                        # Add the item to the list widget
                        list_widget.addItem(item)
                        
                        # Set the checkbox as the widget for this item
                        list_widget.setItemWidget(item, checkbox)

                    layout.addWidget(list_widget)

                    # OK button to confirm selections
                    ok_button = QPushButton("OK", dialog)
                    ok_button.clicked.connect(lambda: self.handle_selected_tags(dialog, list_widget, transaction))
                    layout.addWidget(ok_button)

                    # Show the dialog
                    dialog.exec_()
    def handle_selected_tags(self, dialog, list_widget, transaction):
        """Handle the selected tags after the OK button is clicked."""
        selected_tags = []
        
        # Loop through the items in the QListWidget and check which are selected
        for index in range(list_widget.count()):
            item = list_widget.item(index)
            checkbox = list_widget.itemWidget(item)  # Get the associated checkbox for the item
            if checkbox.isChecked():  # Check if checkbox is selected
                selected_tags.append(item.text())

        # Get the tag dictionaries corresponding to the selected tag names
        tag_dicts = [tags[tag_name] for tag_name in selected_tags if tag_name in tags]
        transaction.set_tags(tag_dicts)

        # Close the dialog after handling
        dialog.accept()
        transactions_observable._notify_observers()
        unsaved_changes.set_data(True)