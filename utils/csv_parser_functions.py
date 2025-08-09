from datetime import datetime
import re
from utils.csv_type_enums import ColumnType


SHEKEL_TO_DOLLARS_EXCHANGE = 3.5 # Default to 3.5

CURRENCY_SYMBOLS = [
    "$",   # Dollar
    "¢",   # Cent
    "£",   # Pound
    "¤",   # Generic currency sign
    "¥",   # Yen / Yuan
    "₠",   # Euro-currency
    "₡",   # Colon
    "₢",   # Cruzeiro
    "₣",   # French Franc
    "₤",   # Lira
    "₥",   # Mill
    "₦",   # Naira
    "₧",   # Peseta
    "₨",   # Rupee
    "₩",   # Won
    "₪",   # Shekel
    "₫",   # Dong
    "€",   # Euro
    "₭",   # Kip
    "₮",   # Tugrik
    "₯",   # Drachma
    "₰",   # German Penny
    "₱",   # Peso
    "₲",   # Guarani
    "₳",   # Austral
    "₴",   # Hryvnia
    "₵",   # Cedi
    "₶",   # Livre Tournois
    "₷",   # Spesmilo
    "₸",   # Tenge
    "₺",   # Turkish Lira
    "₻",   # Nordic Mark
    "₼",   # Azerbaijani Manat
    "₽",   # Russian Ruble
    "₾",   # Georgian Lari
    "₿"    # Bitcoin
]

CURRENCY_PATTERN = "[" + "".join(re.escape(sym) for sym in CURRENCY_SYMBOLS) + "]"

def remove_currency_symbols(text):
    return re.sub(CURRENCY_PATTERN, "", text)

def override_shekels_to_dollars_exchange(value):
    global SHEKEL_TO_DOLLARS_EXCHANGE
    SHEKEL_TO_DOLLARS_EXCHANGE = value

def normalize(s):
    return re.sub(r'\s+', ' ', s.strip())

def parse_date_fmt(value, fmt):
    try:
        return datetime.strptime(value, fmt).strftime("%m/%d/%Y")
    except ValueError:
        return None

def parse_date(value):
    formats = [
        "%m/%d/%Y",
        "%m/%d/%y",
        "%d-%m-%Y",
        "%Y-%m-%d"
    ]
    
    for fmt in formats:
        parsed = parse_date_fmt(value, fmt)
        if parsed is not None:
            return parsed
    
    raise ValueError(f"Date format not recognized: {value}")
    
def parse_float(value):
    try:
        new_value = float(remove_currency_symbols(value).replace(',', '').strip())
    except ValueError:
        new_value = 0 # default to 0 if string parsing goes wrong/null
    return new_value
        

def parse_shekel(value):
    try:
        new_value = float(remove_currency_symbols(value).replace(',', '').strip())
        new_value * SHEKEL_TO_DOLLARS_EXCHANGE
    except ValueError:
        new_value = 0 # defaults to 0 if string parsing goes wrong/null
    return new_value
    
def parse_string(value):
    return normalize(str(value))

def parse_flag(value):
    return normalize(str(value)).lower()

ColumnTypeParsers = {
    # Standard column types
    ColumnType.DATE: parse_date,
    ColumnType.STRING: parse_string,
    ColumnType.FLOAT: parse_float,
    ColumnType.SHEKEL: parse_shekel,
    # Metadata column types
    ColumnType.TYPE_FLAG: parse_flag,
    ColumnType.CURRENCY_FLAG: parse_string,
    ColumnType.AMOUNT_SECOND: parse_float
}

def get_column_data(value, column_type):
    parser = ColumnTypeParsers[column_type]
    return parser(value)