from file_import_tab import FileImportTab
from data_view_tab import DataViewTab
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMessageBox, QMenu
from PyQt5.QtCore import Qt
import qdarkstyle
import os
from docking import GenericDockWidget
from unsaved_changes import unsaved_changes
from load_save_data import save_to_pickle_file
from docks import dock_widgets
from visible_tags import TagSelectionDialog
from DateRangeFilters import DateRangeDialog, start, end
from chart import ChartWidget
from pie import PieChart
from radar import RadarChart
from month_bar import MonthlyBarChart
from tag_bar import TagBarChart
from donut import DonutChart

os.environ['QT_API'] = 'pyqt5'

class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Upload Example")
        self.setGeometry(300, 300, 800, 800)

        self.data_view_dock = GenericDockWidget("Data View", DataViewTab(self), self)
        self.file_import_dock = GenericDockWidget("File Import", FileImportTab(self), self)
        self.chart_pie = GenericDockWidget("Pie Chart", ChartWidget(PieChart(start, end), self), self)
        self.chart_donut = GenericDockWidget("Donut Chart", ChartWidget(DonutChart(start, end), self), self)
        self.chart_radar = GenericDockWidget("Radar Chart", ChartWidget(RadarChart(start, end), self), self)
        self.chart_bar = GenericDockWidget("Tag Bar Chart", ChartWidget(TagBarChart(start, end), self), self)
        self.chart_month_bar = GenericDockWidget("Monthly Bar Chart", ChartWidget(MonthlyBarChart(start, end), self), self)


        self.data_view_dock.closed.connect(self.on_dock_widget_closed)
        self.file_import_dock.closed.connect(self.on_dock_widget_closed)
        self.chart_pie.closed.connect(self.on_dock_widget_closed)
        self.chart_donut.closed.connect(self.on_dock_widget_closed)
        self.chart_radar.closed.connect(self.on_dock_widget_closed)
        self.chart_bar.closed.connect(self.on_dock_widget_closed)
        self.chart_month_bar.closed.connect(self.on_dock_widget_closed)

        self.addDockWidget(Qt.BottomDockWidgetArea, self.data_view_dock)
        self.addDockWidget(Qt.TopDockWidgetArea, self.file_import_dock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.chart_pie)
        self.addDockWidget(Qt.RightDockWidgetArea, self.chart_donut)
        self.addDockWidget(Qt.RightDockWidgetArea, self.chart_radar)
        self.addDockWidget(Qt.RightDockWidgetArea, self.chart_bar)
        self.addDockWidget(Qt.RightDockWidgetArea, self.chart_month_bar)

        dock_widgets.set_data({
            "Data View": self.data_view_dock,
            "File Import": self.file_import_dock,
            "Pie Chart": self.chart_pie,
            "Donut Chart": self.chart_donut,
            "Radar Chart": self.chart_radar,
            "Tag Bar Chart": self.chart_bar,
            "Monthly Bar Chart": self.chart_month_bar
        })

        self.create_menu_bar()
        self.data_view_dock.close()
        self.chart_pie.close()
        self.chart_donut.close()
        self.chart_radar.close()
        self.chart_bar.close()
        self.chart_month_bar.close()

        self.data_view_dock.setFloating(True)
        self.chart_pie.setFloating(True)
        self.chart_donut.setFloating(True)
        self.chart_radar.setFloating(True)
        self.chart_bar.setFloating(True)
        self.chart_month_bar.setFloating(True)

        dock_widgets.add_observer(self.dock_widgets_change)

    def dock_widgets_change(self):
        view_menu = self.menuBar().findChild(QMenu, "View")
        if view_menu:
            view_menu.clear()
            for dock_name in dock_widgets.get_data():
                action = QAction(dock_name, self)
                action.setObjectName(dock_name)
                action.setCheckable(True)
                action.setChecked(dock_widgets.get_data()[dock_name].isVisible())
                action.triggered.connect(self.toggle_dock_widget)
                view_menu.addAction(action)

    def on_dock_widget_closed(self):
        dock_widget = self.sender()
        for name, widget in dock_widgets.get_data().items():
            if widget == dock_widget:
                action = self.findChild(QAction, name)
                if action:
                    action.setChecked(False)
                break

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")

        save_action = QAction("Save", self)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        save_action.triggered.connect(save_to_pickle_file)

        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        view_menu = menu_bar.addMenu("View")
        for dock_name in dock_widgets.get_data():
            action = QAction(dock_name, self)
            action.setObjectName(dock_name)
            action.setCheckable(True)
            action.setChecked(True)
            action.triggered.connect(self.toggle_dock_widget)
            view_menu.addAction(action)
        # Add a menu option to show the tag selection dialog
        
        tag_selection_action = QAction("Enable/Disable Tags", self)
        tag_selection_action.triggered.connect(self.show_tag_selection_dialog)
        date_range_action = QAction("Date Range", self)
        date_range_action.triggered.connect(self.show_date_range_dialog)

        tools_menu = menu_bar.addMenu("Tools")
        tools_menu.addAction(tag_selection_action)
        tools_menu.addAction(date_range_action)

    def show_date_range_dialog(self):
        dialog = DateRangeDialog(self)
        dialog.exec_()

    def show_tag_selection_dialog(self):
        dialog = TagSelectionDialog(self)
        dialog.exec_()

    def toggle_dock_widget(self):
        action = self.sender()
        dock_widget = dock_widgets.get_data()[action.text()]
        if action.isChecked():
            dock_widget.show()
        else:
            dock_widget.close()

    def closeEvent(self, event):
        if unsaved_changes.get_data():
            reply = QMessageBox.question(self, 'Unsaved Changes',
                                         "You have unsaved changes. Do you want to save them before exiting?",
                                         QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                                         QMessageBox.Save)

            if reply == QMessageBox.Save:
                save_to_pickle_file()
                event.accept()
            elif reply == QMessageBox.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    window = App()
    window.show()

    sys.exit(app.exec_())