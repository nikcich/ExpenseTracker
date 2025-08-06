from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from utils.csv_validator import validate_csv
from utils.csv_definitions import all_csv_definitions
from utils.parse_csv import parse_csv_to_transactions
from utils.load_save_data import transactions_observable
from observables.unsaved_changes import unsaved_changes

class FileImportTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Layout for the tab
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)  # Adding margins to the layout
        self.layout.setSpacing(15)  # Adding space between widgets
        
        self.selected_file_definition = None

        # Header Label - "No file selected"
        self.label = QLabel("No file selected", self)
        self.label.setFont(QFont("Arial", 14))
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        # Upload Button
        self.upload_button = QPushButton("Upload File", self)
        self.upload_button.setFont(QFont("Arial", 12))
        self.upload_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: 2px solid #2980b9;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1f6c9c;
            }
        """)
        self.upload_button.clicked.connect(self.upload_file)
        self.layout.addWidget(self.upload_button)

        # Information label (for showing upload status)
        self.info_label = QLabel("", self)
        self.info_label.setFont(QFont("Arial", 12))
        self.info_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.info_label)

        # Spacer to add space before the Parse button
        self.spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(self.spacer)

        # Parse Button (hidden initially)
        self.parse_button = QPushButton("Parse CSV", self)
        self.parse_button.setFont(QFont("Arial", 12))
        self.parse_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: 2px solid #2ecc71;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        self.parse_button.clicked.connect(self.parse_csv)
        self.parse_button.setVisible(False)
        self.layout.addWidget(self.parse_button)

        # Refresh observer (keeping the transaction data updated)
        transactions_observable.add_observer(self.refresh)

    def refresh(self):
        """Refresh the content of this tab."""
        # Clear any widget updates
        self.info_label.setText("")
        self.parse_button.setVisible(False)

    def upload_file(self):
        """Handle file upload and validation."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV files (*.csv)")
        
        if file_path:
            matching_csv = None
            for csv_def in all_csv_definitions:
                if validate_csv(file_path, csv_def):
                    matching_csv = csv_def
                    break

            if matching_csv is not None:
                self.info_label.setText(f"Successfully uploaded {matching_csv['name']}")
                self.label.setText(f"Selected file: {file_path}")
                self.parse_button.setVisible(True)
                self.selected_file_definition = matching_csv
            else:
                self.info_label.setText("Invalid file format")
                self.selected_file_definition = None

    def parse_csv(self):
        """Parse the CSV file and create Transaction objects."""
        file_path = self.label.text().replace("Selected file: ", "")
        if file_path and self.selected_file_definition is not None:
            transactions = parse_csv_to_transactions(file_path, self.selected_file_definition)
            data = transactions_observable.get_data() or {}
            data.update({t.uuid: t for t in transactions})
            transactions_observable.set_data(data)
            self.label.setText("No file selected")
            self.info_label.setText(f"Successfully parsed {len(transactions)} transactions")
            self.parse_button.setVisible(False)
            if len(transactions) > 0:
                unsaved_changes.set_data(True)
