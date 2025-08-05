from enum import Enum, auto

class Role(Enum):
    DATE = auto()
    AMOUNT = auto()
    DESCRIPTION = auto()

class ColumnType(Enum):
    DATE = auto()
    STRING = auto()
    FLOAT = auto()
    TYPE_FLAG = auto()



wf_csv_definition = {
    'name': 'Wells Fargo Spending Report',
    'hasHeaders': True,
    'columns': [
        {'type': ColumnType.DATE, 'index': 2, 'role': Role.DATE},    # Date (date format)
        {'type': ColumnType.STRING, 'index': 5, 'role': Role.DESCRIPTION},  # Description (string)
        {'type': ColumnType.FLOAT, 'index': 7, 'role': Role.AMOUNT},   # Amount (currency/float)
    ],
}

wf_activity_csv_definition = {
    'name': 'Wells Fargo Activity Report',
    'hasHeaders': False,
    'columns': [
        {'type': ColumnType.DATE, 'index': 0, 'role': Role.DATE },    # Date (date format)
        {'type': ColumnType.FLOAT, 'index': 1, 'role': Role.AMOUNT, 'invert': True},   # Amount (currency/float), invert to multiple by -1. Expense tracker means + is anticipated to be expenses and - is income based on frame of reference
        {'type': ColumnType.STRING, 'index': 4, 'role': Role.DESCRIPTION},  # Description
    ],
}

amex_csv_definition = {
    'name': 'American Express Spending Report',
    'hasHeaders': True,
    'columns': [
        {'type': ColumnType.DATE, 'index': 0, 'role': Role.DATE},      # Date (date format)
        {'type': ColumnType.STRING, 'index': 1, 'role': Role.DESCRIPTION},    # Description (string)
        {'type': ColumnType.FLOAT, 'index': 2, 'role': Role.AMOUNT},     # Amount (currency/float)
    ],
}

capital_csv_definition = {
    'name': 'Capital One Activity Report',
    'hasHeaders': True,
    'columns': [
        {'type': ColumnType.STRING, 'index': 1, 'role': Role.DESCRIPTION},    # Description (string)
        {'type': ColumnType.DATE, 'index':   2, 'role': Role.DATE},  # Date (date format)
        {'type': ColumnType.TYPE_FLAG, 'index': 3},    # Type (credit/debit)
        {'type': ColumnType.FLOAT, 'index':  4, 'role': Role.AMOUNT}, # Amount (float)
    ],
}

# Always add new definitions to this list
all_csv_definitions = [wf_csv_definition, wf_activity_csv_definition, amex_csv_definition, capital_csv_definition]