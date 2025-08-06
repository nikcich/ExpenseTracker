from utils.load_save_data import transactions_observable
from PyQt5.QtCore import QDate
from observables.visible_tags import visibleTags
from widgets.transaction_table import TransactionTable  # Assuming the TransactionTable class is in 'transaction_table.py'
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class FilteredTableView(QWidget):
    def __init__(self, parent, start, end):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.start = start
        self.end = end
        start.add_observer(self.on_filters_changed)
        end.add_observer(self.on_filters_changed)
        transactions_observable.add_observer(self.on_filters_changed)
        visibleTags.add_observer(self.on_filters_changed)

        self.transaction_count_label = QLabel(self)
        self.transaction_table = None

        self.refresh()

        transactions_observable.add_observer(self.refresh)

    def on_filters_changed(self):
        self.refresh()

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
        transactions = list(transactions_observable.get_data().values())
        visible_tags = visibleTags.get_data()
        startDate = self.start.get_data()
        endDate = self.end.get_data()

        # Filter transactions by date and visible tags
        filtered = []
        for t in transactions:
            date = QDate.fromString(t.date, 'MM/dd/yyyy')
            if not (startDate <= date <= endDate):
                continue

            # Check if transaction should be visible based on tags
            if not t.tags:
                filtered.append(t)
            else:
                if any(tag['tag_name'] in visible_tags for tag in t.tags):
                    filtered.append(t)


        self.transaction_count_label.setText(f"Number of Transactions: {len(filtered)}")

        # Remove the placeholder label
        if self.transaction_table:
            self.layout.removeWidget(self.transaction_table)
            self.transaction_table.deleteLater()

        # Create and add the updated transaction table
        self.transaction_table = TransactionTable(self, filtered, sliderPos)
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