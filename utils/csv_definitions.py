from utils.csv_meta_handlers import amount_secondary_handler, credit_type_handler, credit_column_handler
from utils.csv_type_enums import ColumnType, Role

wf_csv_definition = {
    'name': 'Wells Fargo Spending Report',
    'hasHeaders': True,
    'columns': {
        Role.DATE: {'type': ColumnType.DATE, 'index': 2, 'format': '%m/%d/%Y'},
        Role.DESCRIPTION: {'type': ColumnType.STRING, 'index': 5},
        Role.AMOUNT: {'type': ColumnType.FLOAT, 'index': 7}
    },
    'metadata': {
        Role.DATE: [],
        Role.DESCRIPTION: [],
        Role.AMOUNT: []
    }
}

wf_activity_csv_definition = {
    'name': 'Wells Fargo Activity Report',
    'hasHeaders': False,
    'columns': {
        Role.DATE: {'type': ColumnType.DATE, 'index': 0, 'format': '%m/%d/%Y'},
        Role.AMOUNT: {'type': ColumnType.FLOAT, 'index': 1, 'invert': True},
        Role.DESCRIPTION: {'type': ColumnType.STRING, 'index': 4}
    },
    'metadata': {
        Role.DATE: [],
        Role.DESCRIPTION: [],
        Role.AMOUNT: []
    }
}

amex_csv_definition = {
    'name': 'American Express Spending Report',
    'hasHeaders': True,
    'columns': {
        Role.DATE: {'type': ColumnType.DATE, 'index': 0, 'format': '%m/%d/%Y'},
        Role.DESCRIPTION: {'type': ColumnType.STRING, 'index': 1},
        Role.AMOUNT: {'type': ColumnType.FLOAT, 'index': 2}
    },
    'metadata': {
        Role.DATE: [],
        Role.DESCRIPTION: [],
        Role.AMOUNT: []
    }
}

capital_csv_definition = {
    'name': 'Capital One Activity Report',
    'hasHeaders': True,
    'columns': {
        Role.DESCRIPTION: {'type': ColumnType.STRING, 'index': 1},
        Role.DATE: {'type': ColumnType.DATE, 'index': 2, 'format': '%m/%d/%y'},
        Role.AMOUNT: {'type': ColumnType.FLOAT, 'index': 4}
    },
    'metadata': {
        Role.DATE: [],
        Role.DESCRIPTION: [],
        Role.AMOUNT: [
            {
                'handler': credit_type_handler,
                'columns': [{'type': ColumnType.TYPE_FLAG, 'index': 3}]
            }
        ]
    }
}

capital_credit_csv_definition = {
    'name': 'Capital One SavorOne Credit Report',
    'hasHeaders': True,
    'columns': {
        Role.DATE: {'type': ColumnType.DATE, 'index': 0, 'format': '%Y-%m-%d'},
        Role.DESCRIPTION: {'type': ColumnType.STRING, 'index': 3},
        Role.AMOUNT: {'type': ColumnType.FLOAT, 'index': 5}
    },
    'metadata': {
        Role.DATE: [],
        Role.DESCRIPTION: [],
        Role.AMOUNT: [
            {
                'handler': credit_column_handler,
                'columns': [{'type': ColumnType.FLOAT, 'index': 6}]
            }
        ]
    }
}

jewland_credit_csv_definitions = {
    'name': 'Max Credit Card Activity Report',
    'hasHeaders': True,
    'columns': {
        Role.DATE: {'type': ColumnType.DATE, 'index': 0, 'format': '%d-%m-%Y' },
        Role.DESCRIPTION: {'type': ColumnType.STRING, 'index': 1 },
        Role.AMOUNT: {'type': ColumnType.SHEKEL, 'index': 5 }
    },
    'metadata': {
        Role.DATE: [],
        Role.DESCRIPTION: [],
        Role.AMOUNT: [
            { 
                'handler': amount_secondary_handler, 
                'columns': [
                    {'type': ColumnType.AMOUNT_SECOND, 'index': 7},
                    {'type': ColumnType.CURRENCY_FLAG, 'index': 8}
                ]
            }
        ]
    }
}

jewland_bank_csv_definitions = {
    'name': 'Bank Leumi Activity Report',
    'hasHeaders': True,
    'columns': {
        Role.DATE: {'type': ColumnType.DATE, 'index': 0, 'format': '%d/%m/%y' },
        Role.DESCRIPTION: {'type': ColumnType.STRING, 'index': 1 },
        Role.AMOUNT: {'type': ColumnType.SHEKEL, 'index': 3 }
    },
    'metadata': {
        Role.DATE: [],
        Role.DESCRIPTION: [],
        Role.AMOUNT: [
            { 
                'handler': credit_column_handler, 
                'columns': [
                    {'type': ColumnType.FLOAT, 'index': 4},
                ]
            }
        ]
    }
}

# Always add new definitions to this list
all_csv_definitions = [wf_csv_definition, wf_activity_csv_definition, amex_csv_definition, capital_credit_csv_definition, capital_csv_definition, jewland_bank_csv_definitions, jewland_credit_csv_definitions]