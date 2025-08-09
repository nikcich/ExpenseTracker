from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QSizePolicy, QCheckBox
)
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp, Qt
from utils.csv_parser_functions import override_shekels_to_dollars_exchange

class ShekelConversionWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Shekel Conversion")

        main_layout = QVBoxLayout(self)

        # Checkbox to enable/disable input
        self.enable_checkbox = QCheckBox("Enable Conversion", self)
        self.enable_checkbox.setChecked(False)  # Enabled by default
        self.enable_checkbox.stateChanged.connect(self.toggle_input_enabled)
        main_layout.addWidget(self.enable_checkbox)

        # Create a horizontal layout for label + input
        row_layout = QHBoxLayout()
        row_layout.setAlignment(Qt.AlignLeft)  # Align entire row to the left

        label = QLabel("Convert amount:", self)
        label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        row_layout.addWidget(label)

        self.amount_input = QLineEdit(self)
        self.amount_input.setEnabled(False)
        regex = QRegExp(r"^[0-9](\.[0-9]{1,2})?$")
        validator = QRegExpValidator(regex, self.amount_input)
        self.amount_input.setValidator(validator)
        self.amount_input.setPlaceholderText("e.g., 3.54")
        self.amount_input.setFixedWidth(80)
        self.amount_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.amount_input.textChanged.connect(self.on_typed_event)
        row_layout.addWidget(self.amount_input)

        main_layout.addLayout(row_layout)

    def toggle_input_enabled(self, state):
        enabled = state == Qt.Checked
        self.amount_input.setEnabled(enabled)

    def on_typed_event(self, text):
        try:
            value = float(text)
            if value >= 0:
                print(f"Updated exchange rate to: {value}")
                override_shekels_to_dollars_exchange(value) # updates the value in csv_definitions
            else:
                print("Invalid input. Reverting to default exchange rate.")
        except ValueError:
            print("Invalid input. Not a number.")
