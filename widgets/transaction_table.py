from PyQt5.QtWidgets import QTableView, QListWidgetItem, QCheckBox, QListWidget, QDialog, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHeaderView, QLabel, QHBoxLayout, QSizePolicy, QPushButton, QMenu, QAction
from PyQt5.QtCore import Qt, QDate
from custom_types.tags import tags
from utils.load_save_data import transactions_observable
from observables.unsaved_changes import unsaved_changes


class CustomTableWidgetItem(QTableWidgetItem):
    def __init__(self, column, text):
        super().__init__(text)
        self.column = column

    def __lt__(self, other):
        column = self.column
        if column == 1:  # Date column
            return QDate.fromString(self.text(), 'yyyy-MM-dd') < QDate.fromString(other.text(), 'yyyy-MM-dd')
        elif column == 3:  # Amount column
            return float(self.text().replace('$', '').replace(',', '')) < float(other.text().replace('$', '').replace(',', ''))
        else:
            return super().__lt__(other)


class TagSelectionDialog(QDialog):
    def __init__(self, parent, transaction):
        super().__init__(parent)
        self.transaction = transaction
        self.setWindowTitle("Select Tags")
        self.setFixedSize(300, 300)
        self.layout = QVBoxLayout(self)
        self.label = QLabel("Select the tags for this transaction:")
        self.layout.addWidget(self.label)
        self.list_widget = QListWidget(self)
        self.populate_list_widget()
        self.layout.addWidget(self.list_widget)
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.handle_selected_tags)
        self.layout.addWidget(self.ok_button)

    def populate_list_widget(self):
        for tag_key, tag_data in tags.items():
            tag_name = tag_data['tag_name']
            tag_exists = any(tag['tag_name'] == tag_name for tag in self.transaction.tags)
            item = QListWidgetItem(tag_name)
            checkbox = QCheckBox(tag_name)
            checkbox.setChecked(tag_exists)
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, checkbox)

    def handle_selected_tags(self):
        selected_tags = []
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            checkbox = self.list_widget.itemWidget(item)
            if checkbox.isChecked():
                selected_tags.append(item.text())
        tag_dicts = [tags[tag_name] for tag_name in selected_tags if tag_name in tags]
        self.transaction.set_tags(tag_dicts)
        self.accept()
        transactions_observable._notify_observers()
        unsaved_changes.set_data(True)


class MultiTagSelectionDialog(QDialog):
    def __init__(self, parent, selected_transactions):
        super().__init__(parent)
        self.selected_transactions = selected_transactions
        self.setWindowTitle("Select Tags for Selected Rows")
        self.setFixedSize(300, 300)
        self.layout = QVBoxLayout(self)
        self.label = QLabel("Select tags for the selected rows:")
        self.layout.addWidget(self.label)
        self.list_widget = QListWidget(self)
        self.populate_list_widget()
        self.layout.addWidget(self.list_widget)
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.handle_selected_tags_for_multiple)
        self.layout.addWidget(self.ok_button)

    def populate_list_widget(self):
        common_tags = self.get_common_tags()
        for tag_key, tag_data in tags.items():
            tag_name = tag_data['tag_name']
            tag_exists_for_all = all(tag_name in [tag['tag_name'] for tag in transaction.tags] for transaction in self.selected_transactions)
            item = QListWidgetItem(tag_name)
            checkbox = QCheckBox(tag_name)
            checkbox.setChecked(tag_exists_for_all)
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, checkbox)

    def get_common_tags(self):
        if not self.selected_transactions:
            return []
        common_tags = set(tag['tag_name'] for tag in self.selected_transactions[0].tags)
        for transaction in self.selected_transactions[1:]:
            transaction_tags = set(tag['tag_name'] for tag in transaction.tags)
            common_tags &= transaction_tags
        return common_tags

    def handle_selected_tags_for_multiple(self):
        selected_tags = []
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            checkbox = self.list_widget.itemWidget(item)
            if checkbox.isChecked():
                selected_tags.append(item.text())
        tag_dicts = [tags[tag_name] for tag_name in selected_tags if tag_name in tags]
        for transaction in self.selected_transactions:
            transaction.set_tags(tag_dicts)
        self.accept()
        transactions_observable._notify_observers()
        unsaved_changes.set_data(True)


class TransactionTable(QWidget):
    def __init__(self, parent, transactions, sliderPos):
        super().__init__(parent)
        self.transactions = transactions
        self.sliderPos = sliderPos
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Tags", "Date", "Description", "Amount"])
        self.table_widget.setSelectionBehavior(QTableView.SelectRows)
        self.table_widget.setSortingEnabled(True)
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_widget.setMinimumWidth(800)
        header = self.table_widget.horizontalHeader()

        self.table_widget.resizeColumnsToContents()
        header.setStretchLastSection(True)
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QVBoxLayout(self)
        layout.addWidget(self.table_widget)
        self.setLayout(layout)
        self.table_widget.cellDoubleClicked.connect(self.on_cell_double_clicked)
        self.table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self.show_context_menu)
        self.refresh()

    def show_context_menu(self, pos):
        context_menu = QMenu(self)
        tag_action = QAction("Select Tags for Selected Rows", self)
        tag_action.triggered.connect(self.select_tags_for_selected_rows)
        context_menu.addAction(tag_action)
        context_menu.exec_(self.table_widget.mapToGlobal(pos))

    def refresh(self):
        self.table_widget.setRowCount(len(self.transactions))
        self.table_widget.verticalScrollBar().setMaximum(len(self.transactions))
        self.table_widget.verticalScrollBar().setValue(self.sliderPos)
        for row, transaction in enumerate(self.transactions):
            formatted_amount = f"${transaction.amount:,.2f}"
            transaction_date = QDate.fromString(transaction.date, 'MM/dd/yyyy')
            self.table_widget.setItem(row, 1, CustomTableWidgetItem(1, transaction_date.toString('yyyy-MM-dd')))
            self.table_widget.setItem(row, 2, CustomTableWidgetItem(2, transaction.description))
            self.table_widget.setItem(row, 3, CustomTableWidgetItem(3, formatted_amount))
            tag_widget = self.create_tag_widget(transaction.tags)
            self.table_widget.setCellWidget(row, 0, tag_widget)
        self.table_widget.verticalScrollBar().setValue(self.sliderPos)

    def create_tag_widget(self, tags):
        tag_widget = QWidget()
        tag_layout = QHBoxLayout(tag_widget)
        tag_layout.setContentsMargins(3, 0, 3, 0)
        tag_layout.setSpacing(5)
        tag_layout.setAlignment(Qt.AlignLeft)
        tag_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        tag_widget.setWindowFlags(Qt.FramelessWindowHint)
        tag_widget.setAttribute(Qt.WA_TranslucentBackground)
        for tag in tags:
            color = tag['color']
            name = tag['tag_name']
            pill = QPushButton(name)
            pill.setStyleSheet(f"""
                background-color: {color};
                border-radius: 10px;
                color: white;
                height: 20px;
                padding-left: 8px;
                padding-right: 8px;
                text-align: center;
                white-space: nowrap;
            """)
            pill.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
            pill.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            tag_layout.addWidget(pill)
        return tag_widget

    def update_table(self, transactions):
        self.transactions = transactions
        self.refresh()

    def match_transaction(self, date, desc, amount):
        if date and desc and amount:
            matching_transactions = [
                trans for trans in self.transactions
                if (QDate.fromString(trans.date, 'MM/dd/yyyy').toString('yyyy-MM-dd') == date and
                    trans.description == desc and
                    f"${trans.amount:,.2f}" == amount)
            ]
        if matching_transactions:
            return matching_transactions[0]
        else:
            return None

    def on_cell_double_clicked(self, row, column):
        if column == 0:
            item = self.table_widget.cellWidget(row, column)
            date = self.table_widget.item(row, 1)
            description = self.table_widget.item(row, 2)
            amount = self.table_widget.item(row, 3)
            if item:
                transaction = self.match_transaction(date.text(), description.text(), amount.text())
                if transaction:
                    dialog = TagSelectionDialog(self, transaction)
                    dialog.exec_()

    def select_tags_for_selected_rows(self):
        selected_rows = self.table_widget.selectionModel().selectedRows()
        selected_transactions = []
        for row in selected_rows:
            date_item = self.table_widget.item(row.row(), 1)
            description_item = self.table_widget.item(row.row(), 2)
            amount_item = self.table_widget.item(row.row(), 3)
            transaction = self.match_transaction(date_item.text(), description_item.text(), amount_item.text())
            if transaction:
                selected_transactions.append(transaction)
        if selected_transactions:
            dialog = MultiTagSelectionDialog(self, selected_transactions)
            dialog.exec_()