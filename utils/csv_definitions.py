from enum import Enum, auto
from datetime import datetime
import re

def normalize(s):
    return re.sub(r'\s+', ' ', s.strip())

class Role(Enum):
    DATE = auto()
    AMOUNT = auto()
    DESCRIPTION = auto()

class ColumnType(Enum):
    DATE_Y = auto()
    DATE_y = auto()
    STRING = auto()
    FLOAT = auto()
    TYPE_FLAG = auto()

def parse_date_fmt(value, fmt):
    try:
        return datetime.strptime(value, fmt).strftime("%m/%d/%Y")
    except ValueError:
        raise ValueError()

def parse_date_Y(value):
    try:
        return parse_date_fmt(value, "%m/%d/%Y")
    except ValueError:
        raise ValueError("Invalid date format provided; Y")

def parse_date_y(value):
    try:
        return parse_date_fmt(value, "%m/%d/%y")
    except ValueError:
        raise ValueError("Invalid date format provided; y")
    
def parse_float(value):
    try:
        return float(value.replace('$', '').replace(',', '').strip())
    except ValueError:
        raise ValueError("Invalid amount provided")
    
def parse_string(value):
    return normalize(str(value))

def parse_flag(value):
    return normalize(str(value)).lower()

ColumnTypeParsers = {
    ColumnType.DATE_Y: parse_date_Y,
    ColumnType.DATE_y: parse_date_y,
    ColumnType.STRING: parse_string,
    ColumnType.FLOAT: parse_float,
    ColumnType.TYPE_FLAG: parse_flag,
}

wf_csv_definition = {
    'name': 'Wells Fargo Spending Report',
    'hasHeaders': True,
    'columns': [
        {'type': ColumnType.DATE_Y, 'index': 2, 'role': Role.DATE},    # Date (date format)
        {'type': ColumnType.STRING, 'index': 5, 'role': Role.DESCRIPTION},  # Description (string)
        {'type': ColumnType.FLOAT, 'index': 7, 'role': Role.AMOUNT},   # Amount (currency/float)
    ],
}

wf_activity_csv_definition = {
    'name': 'Wells Fargo Activity Report',
    'hasHeaders': False,
    'columns': [
        {'type': ColumnType.DATE_Y, 'index': 0, 'role': Role.DATE },    # Date (date format)
        {'type': ColumnType.FLOAT, 'index': 1, 'role': Role.AMOUNT, 'invert': True},   # Amount (currency/float), invert to multiple by -1. Expense tracker means + is anticipated to be expenses and - is income based on frame of reference
        {'type': ColumnType.STRING, 'index': 4, 'role': Role.DESCRIPTION},  # Description
    ],
}

amex_csv_definition = {
    'name': 'American Express Spending Report',
    'hasHeaders': True,
    'columns': [
        {'type': ColumnType.DATE_Y, 'index': 0, 'role': Role.DATE},      # Date (date format)
        {'type': ColumnType.STRING, 'index': 1, 'role': Role.DESCRIPTION},    # Description (string)
        {'type': ColumnType.FLOAT, 'index': 2, 'role': Role.AMOUNT},     # Amount (currency/float)
    ],
}

capital_csv_definition = {
    'name': 'Capital One Activity Report',
    'hasHeaders': True,
    'columns': [
        {'type': ColumnType.STRING, 'index': 1, 'role': Role.DESCRIPTION},    # Description (string)
        {'type': ColumnType.DATE_y, 'index':   2, 'role': Role.DATE},  # Date (date format)
        {'type': ColumnType.TYPE_FLAG, 'index': 3},    # Type (credit/debit)
        {'type': ColumnType.FLOAT, 'index':  4, 'role': Role.AMOUNT}, # Amount (float)
    ],
}

# Always add new definitions to this list
all_csv_definitions = [wf_csv_definition, wf_activity_csv_definition, amex_csv_definition, capital_csv_definition]