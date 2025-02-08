from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton
from observable import Observable
from date_range import DateRangeSelector

start = Observable()
start.set_data(QDate.currentDate().addYears(-1))
end = Observable()
end.set_data(QDate.currentDate())

class DateRangeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select date range")

        layout = QVBoxLayout(self)

        self.start = start
        self.end = end

        self.dateRange = DateRangeSelector(self.start.get_data(), self.end.get_data(), self.onDateRangeChanged)

        layout.addWidget(self.dateRange)

        # OK button to confirm selection
        ok_button = QPushButton("OK", self)
        ok_button.clicked.connect(self.close)
        layout.addWidget(ok_button)

    def onDateRangeChanged(self, s, e):
        if s != start.get_data():
            start.set_data(s)
        if e != end.get_data():
            end.set_data(e)
