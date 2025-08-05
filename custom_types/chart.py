from PyQt5 import QtCore, QtWidgets
from utils.load_save_data import transactions_observable
from PyQt5.QtCore import QDate
from widgets.sum_label import TotalAmountLabel
from observables.DateRangeFilters import start, end

class ChartWidget(QtWidgets.QWidget):
    def __init__(self, chart, parent=None):
        super().__init__(parent)
        self.start = start
        self.end = end
        self.chart = chart

        # Create a label for the no data message
        self.no_data_label = QtWidgets.QLabel("No transactions available for the selected date range.", self)
        self.no_data_label.setAlignment(QtCore.Qt.AlignCenter)
        self.no_data_label.setStyleSheet("font-size: 16px; color: red;")
        self.data_sum_label = TotalAmountLabel(self.start, self.end)

        # Layout setup for the entire widget
        vlayout = QtWidgets.QVBoxLayout(self)
        vlayout.addWidget(self.data_sum_label, stretch=0)
        vlayout.addWidget(self.no_data_label, stretch=1)
        vlayout.addWidget(self.chart, stretch=1)

        # Initially hide the chart if there is no data
        self.no_data_label.setVisible(False)
        self.chart.setVisible(False)
        self.show_graph()

        self.start.add_observer(self.onDateRangeChanged)
        self.end.add_observer(self.onDateRangeChanged)

    def onDateRangeChanged(self):
        self.show_graph()

    def get_filtered_transactions(self):
        return [
            transaction for transaction in transactions_observable.get_expenses()
            if self.start.get_data() <= QDate.fromString(transaction.date, 'MM/dd/yyyy') <= self.end.get_data()
        ]

    def show_graph(self):
        filtered_transactions = self.get_filtered_transactions()
        
        if len(filtered_transactions) == 0:
            self.no_data_label.setVisible(True)  # Show the no data message
            self.data_sum_label.setVisible(False)
            self.chart.setVisible(False)
        else:
            self.data_sum_label.setVisible(True)
            self.no_data_label.setVisible(False)  # Hide the no data message
            self.chart.setVisible(True)