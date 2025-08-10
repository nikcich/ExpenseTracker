from utils.csv_parser_functions import get_column_data

def get_column_value(column, row):
    column_index = column['index']
    col_value = row[column_index]
    converted_value = get_column_data(col_value, column)

    return converted_value

########################################
####### Metadata Handlers ##############
########################################

def credit_type_handler(meta_cols, row, value):
    column_value = get_column_value(meta_cols[0], row)
    if str(column_value).lower() == 'credit':
        return -value
    return value

def amount_secondary_handler(meta_cols, row, value):                 
    amount_col = meta_cols[0]
    currency_col = meta_cols[1]
    amount_value = get_column_value(amount_col, row)
    currency_value = get_column_value(currency_col, row)
    is_dollar = str(currency_value) == '$'

    if is_dollar:
        return amount_value
    return value

def credit_column_handler(meta_cols, row, value):
    column_value = get_column_value(meta_cols[0], row)
    if column_value is not None and isinstance(column_value, float) and column_value > 0:
        return -column_value
    return value