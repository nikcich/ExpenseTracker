from PyQt5.QtWidgets import QHBoxLayout, QLabel, QDialog, QVBoxLayout, QPushButton, QCheckBox, QListWidget, QListWidgetItem
from tags import tags 
from observable import Observable

# Observable to store the selected tags
visibleTags = Observable()
visibleTags.set_data([tag_data['tag_name'] for tag_data in tags.values()])

class TagSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Tags")
        self.setFixedSize(300, 400)  # Adjust size as needed

        layout = QVBoxLayout(self)

        # Label for instructions
        label = QLabel("Select tags for the transaction:")
        layout.addWidget(label)

        # Create a QListWidget to hold the checkboxes
        self.list_widget = QListWidget(self)
        
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
            self.list_widget.addItem(item)  # Add the item to the list widget
            
            # Set the checkbox as the widget for the item
            self.list_widget.setItemWidget(item, checkbox)
        
        layout.addWidget(self.list_widget)

        # Create a horizontal layout for the check/uncheck all buttons
        button_layout = QHBoxLayout()

        # Check All button
        check_all_button = QPushButton("Check All", self)
        check_all_button.clicked.connect(self.check_all)
        button_layout.addWidget(check_all_button)

        # Uncheck All button
        uncheck_all_button = QPushButton("Uncheck All", self)
        uncheck_all_button.clicked.connect(self.uncheck_all)
        button_layout.addWidget(uncheck_all_button)

        layout.addLayout(button_layout)

        # OK button to confirm selection
        ok_button = QPushButton("OK", self)
        ok_button.clicked.connect(self.handle_tag_selection)
        layout.addWidget(ok_button)

    def check_all(self):
        """Check all checkboxes"""
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            checkbox = self.list_widget.itemWidget(item)
            checkbox.setChecked(True)

    def uncheck_all(self):
        """Uncheck all checkboxes"""
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            checkbox = self.list_widget.itemWidget(item)
            checkbox.setChecked(False)

    def handle_tag_selection(self):
        """Handles the selected tags after pressing OK"""
        selected_tags = []

        # Loop through the items in the list widget and check which checkboxes are selected
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            checkbox = self.list_widget.itemWidget(item)  # Get the associated checkbox for the item
            if checkbox.isChecked():  # If the checkbox is checked, add the tag to the list
                selected_tags.append(item.text())

        # Update the observable with the selected tags
        visibleTags.set_data(selected_tags)
        self.accept()  # Close the dialog