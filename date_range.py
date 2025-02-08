from PyQt5.QtWidgets import QWidget, QVBoxLayout, QDateEdit, QLabel, QHBoxLayout, QSizePolicy

class DateRangeSelector(QWidget):
    def __init__(self, start, end, cb):
        super().__init__()

        self.cb = cb
        # Initialize the layout
        self.layout = QVBoxLayout(self)

        # Create a label to display the selected date range
        self.range_label = QLabel(f"Selected Date Range: {start.toString('yyyy-MM-dd')} to {end.toString('yyyy-MM-dd')}")

        self.layout.addWidget(self.range_label)

        # Create a horizontal layout for the start date and end date
        date_layout = QHBoxLayout()

        # Create a QDateEdit widget for the start date
        self.start_date_picker = QDateEdit(self)
        self.start_date_picker.setDate(start)  # Default to current date
        self.start_date_picker.setDisplayFormat("yyyy-MM-dd")
        self.start_date_picker.setCalendarPopup(True)  # Show calendar popup
        self.start_date_picker.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Prevent excessive vertical stretching
        date_layout.addWidget(QLabel("Start Date:"))
        date_layout.addWidget(self.start_date_picker)

        # Create a QDateEdit widget for the end date
        self.end_date_picker = QDateEdit(self)
        self.end_date_picker.setDate(end)  # Default to current date
        self.end_date_picker.setDisplayFormat("yyyy-MM-dd")
        self.end_date_picker.setCalendarPopup(True)  # Show calendar popup
        self.end_date_picker.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Prevent excessive vertical stretching
        date_layout.addWidget(QLabel("End Date:"))
        date_layout.addWidget(self.end_date_picker)

        # Add the date range layout to the main layout
        self.layout.addLayout(date_layout)

        # Connect the date change signals to the range update method
        self.start_date_picker.dateChanged.connect(self.update_range)
        self.end_date_picker.dateChanged.connect(self.update_range)

        # Set the layout
        self.setLayout(self.layout)
        self.setWindowTitle("Date Range Selector")
        self.resize(400, 150)

    def update_range(self):
        # Get the selected start and end date
        start_date = self.start_date_picker.date()
        end_date = self.end_date_picker.date()

        # Check if the end date is before the start date
        if start_date > end_date:
            # Block the signals temporarily to prevent the invalid date change
            self.end_date_picker.blockSignals(True)
            
            # Revert the end date to the last valid value (before the invalid change)
            self.end_date_picker.setDate(start_date)
            
            # Re-enable the signals
            self.end_date_picker.blockSignals(False)
        else:
            # Update the range label with the selected dates
            self.range_label.setText(f"Selected Date Range: {start_date.toString('yyyy-MM-dd')} to {end_date.toString('yyyy-MM-dd')}")
        
        # Call the callback with the new range
        self.cb(start_date, end_date)
