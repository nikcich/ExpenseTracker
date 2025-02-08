from PyQt5 import QtCore, QtWidgets
from load_save_data import transactions_observable
from pie import PieChart
from date_range import DateRangeSelector
from PyQt5.QtCore import QDate
from observable import Observable
from donut import DonutChart
from radar import RadarChart
from tag_bar import TagBarChart
from month_bar import MonthlyBarChart
from visible_tags import TagSelectionButton
from sum_label import TotalAmountLabel

class Charts(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.start = Observable()
        self.start.set_data(QDate.currentDate().addYears(-1))
        self.end = Observable()
        self.end.set_data(QDate.currentDate())

        # Date Range Selector
        self.dateRange = DateRangeSelector(self.start.get_data(), self.end.get_data(), self.onDateRangeChanged)

        self.tagSelect = TagSelectionButton()

        # Create the chart instances
        self.pie = PieChart(self.start, self.end)
        self.donut = DonutChart(self.start, self.end)
        self.radar = RadarChart(self.start, self.end)
        self.bar = TagBarChart(self.start, self.end)
        self.month_bar = MonthlyBarChart(self.start, self.end)

        # Create checkboxes for each chart
        self.pie_checkbox = QtWidgets.QCheckBox("Show Pie Chart", self)
        self.donut_checkbox = QtWidgets.QCheckBox("Show Donut Chart", self)
        self.radar_checkbox = QtWidgets.QCheckBox("Show Radar Chart", self)
        self.bar_checkbox = QtWidgets.QCheckBox("Show Tag Bar Chart", self)
        self.month_bar_checkbox = QtWidgets.QCheckBox("Show Monthly Bar Chart", self)

        # Set default states for the checkboxes (checked by default)
        self.pie_checkbox.setChecked(False)
        self.donut_checkbox.setChecked(True)
        self.radar_checkbox.setChecked(False)
        self.bar_checkbox.setChecked(False)
        self.month_bar_checkbox.setChecked(False)

        # Connect the checkbox states to their respective chart visibility
        self.pie_checkbox.toggled.connect(self.toggle_pie_chart)
        self.donut_checkbox.toggled.connect(self.toggle_donut_chart)
        self.radar_checkbox.toggled.connect(self.toggle_radar_chart)
        self.bar_checkbox.toggled.connect(self.toggle_bar_chart)
        self.month_bar_checkbox.toggled.connect(self.toggle_month_bar_chart)

        # Create a horizontal layout for the checkboxes
        checkbox_layout = QtWidgets.QHBoxLayout()
        checkbox_layout.addWidget(self.pie_checkbox)
        checkbox_layout.addWidget(self.donut_checkbox)
        checkbox_layout.addWidget(self.radar_checkbox)
        checkbox_layout.addWidget(self.bar_checkbox)
        checkbox_layout.addWidget(self.month_bar_checkbox)

        # Create a label for the no data message
        self.no_data_label = QtWidgets.QLabel("No transactions available for the selected date range.", self)
        self.no_data_label.setAlignment(QtCore.Qt.AlignCenter)
        self.no_data_label.setStyleSheet("font-size: 16px; color: red;")

        self.no_chart_label = QtWidgets.QLabel("No chart selected.", self)
        self.no_chart_label.setAlignment(QtCore.Qt.AlignCenter)
        self.no_chart_label.setStyleSheet("font-size: 16px; color: red;")

        self.data_sum_label = TotalAmountLabel(self.start, self.end)

        # Layout setup for the entire widget
        vlayout = QtWidgets.QVBoxLayout(self)
        vlayout.addWidget(self.tagSelect, stretch=0)
        vlayout.addWidget(self.dateRange, stretch=0)
        vlayout.addLayout(checkbox_layout)  # Add the horizontal checkbox layout
        vlayout.addWidget(self.data_sum_label, stretch=0)
        vlayout.addWidget(self.no_data_label, stretch=1)  # Add the no data label
        vlayout.addWidget(self.no_chart_label, stretch=1)
        vlayout.addWidget(self.pie, stretch=1)
        vlayout.addWidget(self.donut, stretch=1)
        vlayout.addWidget(self.radar, stretch=1)
        vlayout.addWidget(self.bar, stretch=1)
        vlayout.addWidget(self.month_bar, stretch=1)

        # Initially hide the charts if there is no data
        self.no_data_label.setVisible(False)
        self.no_chart_label.setVisible(False)
        self.toggle_pie_chart(self.pie_checkbox.isChecked())
        self.toggle_donut_chart(self.donut_checkbox.isChecked())
        self.toggle_radar_chart(self.radar_checkbox.isChecked())
        self.toggle_bar_chart(self.bar_checkbox.isChecked())
        self.toggle_month_bar_chart(self.month_bar_checkbox.isChecked())
        self.show_graph()

    def onDateRangeChanged(self, start, end):
        if start != self.start.get_data():
            self.start.set_data(start)
        if end != self.end.get_data():
            self.end.set_data(end)
        self.show_graph()

    def get_filtered_transactions(self):
        return [
            transaction for transaction in transactions_observable.get_data()
            if self.start.get_data() <= QDate.fromString(transaction.date, 'MM/dd/yyyy') <= self.end.get_data()
        ]

    def show_graph(self):
        filtered_transactions = self.get_filtered_transactions()
        
        if len(filtered_transactions) == 0:
            self.no_data_label.setVisible(True)  # Show the no data message
            self.no_chart_label.setVisible(False)
            self.data_sum_label.setVisible(False)

            self.pie.setVisible(False)
            self.donut.setVisible(False)
            self.radar.setVisible(False)
            self.bar.setVisible(False)
            self.month_bar.setVisible(False)
        else:
            self.data_sum_label.setVisible(True)
            self.no_data_label.setVisible(False)  # Hide the no data message
            if not self.pie_checkbox.isChecked() and not self.donut_checkbox.isChecked() and not self.radar_checkbox.isChecked() and not self.bar_checkbox.isChecked() and not self.month_bar_checkbox.isChecked():
                self.no_chart_label.setVisible(True)
            else:
                self.no_chart_label.setVisible(False)
            
            self.pie.setVisible(self.pie_checkbox.isChecked())
            self.donut.setVisible(self.donut_checkbox.isChecked())
            self.radar.setVisible(self.radar_checkbox.isChecked())
            self.bar.setVisible(self.bar_checkbox.isChecked())
            self.month_bar.setVisible(self.month_bar_checkbox.isChecked())
            

    def toggle_pie_chart(self, checked):
        self.show_graph()

    def toggle_donut_chart(self, checked):
        self.show_graph()


    def toggle_radar_chart(self, checked):
        self.show_graph()

    def toggle_bar_chart(self, checked):
        self.show_graph()

    def toggle_month_bar_chart(self, checked):
        self.show_graph()