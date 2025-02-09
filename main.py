from widgets.file_import_tab import FileImportTab
from widgets.data_view_tab import DataViewTab
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMessageBox, QMenu
from PyQt5.QtCore import Qt
import qdarkstyle
import os
from custom_types.docking import GenericDockWidget
from observables.unsaved_changes import unsaved_changes
from utils.load_save_data import save_to_pickle_file
from observables.docks import dock_widgets
from observables.visible_tags import TagSelectionDialog
from observables.DateRangeFilters import DateRangeDialog, start, end
from custom_types.chart import ChartWidget
from widgets.pie import PieChart
from widgets.radar import RadarChart
from widgets.month_bar import MonthlyBarChart
from widgets.tag_bar import TagBarChart
from widgets.donut import DonutChart
from widgets.heat import DailyHeatmapChart
from widgets.month_stacked import MonthlyStackedBarChart

sys.path.append('./')

os.environ['QT_API'] = 'pyqt5'

class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Expense Tracker")
        self.setGeometry(300, 300, 1000, 800)

        docks = {
            "Data View": GenericDockWidget("Data View", DataViewTab(self), self),
            "File Import": GenericDockWidget("File Import", FileImportTab(self), self),
            "Pie Chart": GenericDockWidget("Pie Chart", ChartWidget(PieChart(start, end), self), self),
            "Donut Chart": GenericDockWidget("Donut Chart", ChartWidget(DonutChart(start, end), self), self),
            "Radar Chart": GenericDockWidget("Radar Chart", ChartWidget(RadarChart(start, end), self), self),
            "Tag Bar Chart": GenericDockWidget("Tag Bar Chart", ChartWidget(TagBarChart(start, end), self), self),
            "Monthly Bar Chart": GenericDockWidget("Monthly Bar Chart", ChartWidget(MonthlyBarChart(start, end), self), self),
            "Daily Heatmap": GenericDockWidget("Daily Heatmap", DailyHeatmapChart(start, end), self),
            "Monthly Stacked By Tags": GenericDockWidget("Monthly Stacked By Tags", MonthlyStackedBarChart(start, end), self)
        }

        dock_widgets.set_data(docks)
        dock_widgets.add_observer(self.dock_widgets_change)
        self.create_menu_bar()

        default_open = ["File Import"]

        for key in docks:
            docks[key].closed.connect(self.on_dock_widget_closed)
            if key not in default_open:
                docks[key].close()
                docks[key].setFloating(True)
            self.addDockWidget(Qt.TopDockWidgetArea, docks[key])
            

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