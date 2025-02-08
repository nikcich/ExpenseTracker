from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtCore import pyqtSignal

class GenericDockWidget(QDockWidget):
    closed = pyqtSignal()  # Signal emitted when the dock widget is closed

    def __init__(self, title, widget, parent=None):
        super().__init__(title, parent)
        self.setWidget(widget)
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetClosable)
        self.resize(700,700)

    def closeEvent(self, event):
        self.closed.emit()  # Emit the closed signal
        super().closeEvent(event)  # Call the base class implementation

# dock_widget = GenericDockWidget("Sample Dock", sample_widget, self)
# self.addDockWidget(Qt.RightDockWidgetArea, dock_widget)

