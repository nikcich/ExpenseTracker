from datetime import datetime
import re
from utils.csv_type_enums import ColumnType


SHEKEL_TO_DOLLARS_EXCHANGE = 3.5 # Default to 3.5

def override_shekels_to_dollars_exchange(value):
    global SHEKEL_TO_DOLLARS_EXCHANGE
    SHEKEL_TO_DOLLARS_EXCHANGE = value

def normalize(s):
    return re.sub(r'\s+', ' ', s.strip())

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

def parse_date_jew(value):
    try:
        return parse_date_fmt(value, "%d-%m-%Y")
    except ValueError:
        raise ValueError("Invalid date format provided; jew")
    
def parse_float(value):
    try:
        return float(value.replace('$', '').replace(',', '').strip())
    except ValueError:
        raise ValueError("Invalid amount provided")

def parse_shekel(value):
    try:
        return float(value.replace('$', '').replace(',', '').strip()) * SHEKEL_TO_DOLLARS_EXCHANGE
    except ValueError:
        raise ValueError("Invalid amount provided")
    
def parse_string(value):
    return normalize(str(value))

def parse_flag(value):
    return normalize(str(value)).lower()

ColumnTypeParsers = {
    # Standard column types
    ColumnType.DATE_Y: parse_date_Y,
    ColumnType.DATE_y: parse_date_y,
    ColumnType.STRING: parse_string,
    ColumnType.FLOAT: parse_float,
    ColumnType.SHEKEL: parse_shekel,
    ColumnType.DATE_JEW: parse_date_jew,
    # Metadata column types
    ColumnType.TYPE_FLAG: parse_flag,
    ColumnType.CURRENCY_FLAG: parse_string,
    ColumnType.AMOUNT_SECOND: parse_float
}

def get_column_data(value, column_type):
    parser = ColumnTypeParsers[column_type]
    return parser(value)