from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QDateEdit, QLabel
from PyQt5.QtCore import QDate

class DatePickerExample(QWidget):
    def __init__(self, cb):
        super().__init__()

        # Initialize the layout
        self.layout = QWidget(self)

        # Create a label to display the selected date
        self.label = QLabel("Selected Date: ", self)
        self.layout.addWidget(self.label)

        # Create a QDateEdit widget (a date picker)
        self.date_picker = QDateEdit(self)
        self.date_picker.setDate(QDate.currentDate())  # Set the current date as default
        self.date_picker.setDisplayFormat("yyyy-MM-dd")  # Display format (Year-Month-Day)
        self.date_picker.setCalendarPopup(True)  # Show calendar popup when clicked
        self.layout.addWidget(self.date_picker)

        # Connect the date changed signal to a slot
        self.date_picker.dateChanged.connect(self.on_date_changed)
        self.cb = cb

        # Set the layout
        self.setLayout(self.layout)
        self.setWindowTitle("PyQt5 Date Picker Example")
        self.resize(300, 100)

    def on_date_changed(self, date):
        # Update the label when the date is changed
        dt = date.toString('yyyy-MM-dd')
        self.label.setText(f"Selected Date: {dt}")
        self.cb(date)
