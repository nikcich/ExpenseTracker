from enum import Enum, auto

class Role(Enum):
    DATE = auto()
    AMOUNT = auto()
    DESCRIPTION = auto()

class ColumnType(Enum):
    # Standard column types
    DATE_Y = auto()
    DATE_y = auto()
    DATE_JEW = auto()
    STRING = auto()
    FLOAT = auto()
    SHEKEL = auto()
    # Metadata column types
    TYPE_FLAG = auto()
    AMOUNT_SECOND = auto()
    CURRENCY_FLAG = auto()