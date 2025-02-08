from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QPushButton, QDialog, QCheckBox, QHBoxLayout, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
from tags import tags  # Assuming the 'tags' dictionary is imported
from observable import Observable

# Observable to store the selected tags
visibleTags = Observable()
visibleTags.set_data([tag_data['tag_name'] for tag_data in tags.values()])

class TagSelectionButton(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the button
        self.button = QPushButton("Enable/Disable Tags", self)
        self.button.clicked.connect(self.open_tag_selection_dialog)

        # Layout for the button widget
        layout = QVBoxLayout(self)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def open_tag_selection_dialog(self):
        """Opens the tag selection dialog with checkboxes for each tag"""
        # Create a dialog to display the checkboxes
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Tags")
        dialog.setFixedSize(300, 400)  # Adjust size as needed

        layout = QVBoxLayout(dialog)

        # Label for instructions
        label = QLabel("Select tags for the transaction:")
        layout.addWidget(label)

        # Create a QListWidget to hold the checkboxes
        list_widget = QListWidget(dialog)
        
        # Add checkboxes for each tag in the 'tags' dictionary
        for tag_key, tag_data in tags.items():
            tag_name = tag_data['tag_name']
            color = tag_data['color']
            
            # Create a checkbox for each tag
            checkbox = QCheckBox(tag_name)
            checkbox.setStyleSheet(f"color: {color};")  # Set the color of the text to the tag's color
            
            # Check if the tag is in the visibleTags list and set the checkbox accordingly
            checkbox.setChecked(tag_name in visibleTags.get_data())

            item = QListWidgetItem(tag_name)  # Create a list widget item for each tag
            list_widget.addItem(item)  # Add the item to the list widget
            
            # Set the checkbox as the widget for the item
            list_widget.setItemWidget(item, checkbox)
        
        layout.addWidget(list_widget)

        # OK button to confirm selection
        ok_button = QPushButton("OK", dialog)
        ok_button.clicked.connect(lambda: self.handle_tag_selection(dialog, list_widget))
        layout.addWidget(ok_button)

        # Show the dialog
        dialog.exec_()

    def handle_tag_selection(self, dialog, list_widget):
        """Handles the selected tags after pressing OK"""
        selected_tags = []

        # Loop through the items in the list widget and check which checkboxes are selected
        for index in range(list_widget.count()):
            item = list_widget.item(index)
            checkbox = list_widget.itemWidget(item)  # Get the associated checkbox for the item
            if checkbox.isChecked():  # If the checkbox is checked, add the tag to the list
                selected_tags.append(item.text())

        # Update the observable with the selected tags
        visibleTags.set_data(selected_tags)
        dialog.accept()  # Close the dialog
