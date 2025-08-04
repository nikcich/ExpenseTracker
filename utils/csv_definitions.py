wf_csv_definition = {
    'headers': [
        "Master Category", "Subcategory", "Date", "Location", "Payee", 
        "Description", "Payment Method", "Amount", ''
    ],
    'columns': [
        {'type': 'string', 'index': 0},  # Master Category (string)
        {'type': 'string', 'index': 1},  # Subcategory (string)
        {'type': 'date', 'index': 2},    # Date (date format)
        {'type': 'string', 'index': 3},  # Location (string)
        {'type': 'string', 'index': 4},  # Payee (string)
        {'type': 'string', 'index': 5},  # Description (string)
        {'type': 'string', 'index': 6},  # Payment Method (string)
        {'type': 'float', 'index': 7},   # Amount (currency/float)
        {'type': 'string', 'index': 8},  # Empty
    ],
    'date_header': 'Date',
    'amount_header': 'Amount',
    'description_header': 'Description'
}

amex_csv_definition = {
    'headers': [
        "Date", "Description", "Amount"
    ],
    'columns': [
        {'type': 'date', 'index': 0},      # Date (date format)
        {'type': 'string', 'index': 1},    # Description (string)
        {'type': 'float', 'index': 2},     # Amount (currency/float)
    ],
    'date_header': 'Date',
    'amount_header': 'Amount',
    'description_header': 'Description'
}

capital_csv_definition = {
    'headers': [
        "Account Number", "Transaction Description","Transaction Date", "Transaction Type","Transaction Amount","Balance"
    ],
    'columns': [
        {'type': 'string', 'index': 0},    # Description (string)
        {'type': 'string', 'index': 1},    # Description (string)
        {'type': 'date', 'index':   2},  # Date (date format)
        {'type': 'string', 'index': 3},    # Type (currency/float)
        {'type': 'float', 'index':  4},     # Amount (float)
        {'type': 'float', 'index':  5},    # Description (string)
    ],
    'date_header': 'Transaction Date',
    'amount_header': 'Transaction Amount',
    'description_header': 'Transaction Description',
    'type_flag_header': 'Transaction Type'
}