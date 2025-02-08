from file_import_tab import FileImportTab
from data_view_tab import DataViewTab
import sys
from PyQt5.QtWidgets import QApplication, QTabWidget, QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTextStream
import qdarkstyle
import os
from header_banner import HeaderBanner
from charts import Charts

os.environ['QT_API'] = 'pyqt5'

class App(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("File Upload Example")
        self.setGeometry(100, 100, 800, 600)

        # Create a central widget for the layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a QVBoxLayout for the central widget
        layout = QVBoxLayout(central_widget)

        # Create a QTabWidget (tabs)
        self.tabs = QTabWidget(self)

        # Create instances of the tabs
        self.data_view_tab = DataViewTab(self.tabs)
        self.file_import_tab = FileImportTab(self.tabs)
        # Create an instance of the Charts widget
        self.charts = Charts(self.tabs)        

        # Add tabs to the tab widget
        self.tabs.addTab(self.data_view_tab, "Data View")
        self.tabs.addTab(self.file_import_tab, "File Import View")
        self.tabs.addTab(self.charts, "Charts")

        self.header_banner = HeaderBanner(central_widget)

        # Add the header banner and the tabs to the layout
        layout.addWidget(self.header_banner)  # Add header first (it will stay on top)
        layout.addWidget(self.tabs)  # Add the tab widget below the header

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setStyleSheet(qdarkstyle.load_stylesheet())
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    window = App()

    # Show the window
    window.show()

    # Run the application
    sys.exit(app.exec_())