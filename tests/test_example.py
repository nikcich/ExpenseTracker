import unittest
from utils.parse_csv import parse_csv_to_transactions
from utils.csv_definitions import amex_csv_definition, wf_activity_csv_definition, wf_csv_definition

class TestParseCSVToTransactions(unittest.TestCase):
    def test_amex_csv_definition_parse(self):
        file_path = './tests/amex_activity_example.csv'

        try:
            parse_csv_to_transactions(file_path, amex_csv_definition)
        except Exception as e:
            self.fail(f"An exception was thrown: {e}")

    def test_wf_activity_csv_definition_parse(self):
        file_path = './tests/wf_activity_example.csv'

        try:
            parse_csv_to_transactions(file_path, wf_activity_csv_definition)
        except Exception as e:
            self.fail(f"An exception was thrown: {e}")

    def test_wf_spending_report_csv_definition_parse(self):
        file_path = './tests/wf_spending_report_example.csv'

        try:
            parse_csv_to_transactions(file_path, wf_csv_definition)
        except Exception as e:
            self.fail(f"An exception was thrown: {e}")