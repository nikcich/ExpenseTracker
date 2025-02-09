from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from observables.unsaved_changes import unsaved_changes
from utils.load_save_data import save_to_pickle_file

class HeaderBanner(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        # Create the header banner label
        self.header_banner = QPushButton("Save Changes", self)
        self.header_banner.setStyleSheet("background-color: #3498db; color: white; font-size: 18px; padding: 10px;")
        self.header_banner.clicked.connect(self.save_data)
        self.layout.addWidget(self.header_banner)
        self.refresh()
        unsaved_changes.add_observer(self.refresh)

    def refresh(self, hasUnsavedChanges = False):
        self.header_banner.setVisible(hasUnsavedChanges)

    def save_data(self):
        save_to_pickle_file()