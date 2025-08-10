import unittest
from utils.parse_csv import parse_csv_to_transactions
from utils.csv_definitions import amex_csv_definition, wf_activity_csv_definition, wf_csv_definition
from utils.csv_validator import validate_csv

expected_transactions = [
    {'date': '02/15/2023', 'description': 'Groceries', 'amount': 45.67},
    {'date': '02/14/2023', 'description': 'Restaurant', 'amount': 21.99},
    {'date': '02/13/2023', 'description': 'Entertainment', 'amount': 15.00},
    {'date': '02/12/2023', 'description': 'Transportation', 'amount': 8.50}
]

class TestParseCSVToTransactions(unittest.TestCase):
    def test_amex_csv_definition_parse(self):
        file_path = './tests/mocks/good/amex_activity_good_example.csv'

        try:
            transactions = parse_csv_to_transactions(file_path, amex_csv_definition)
        except Exception as e:
            self.fail(f"An exception was thrown: {e}")

        self.assertEqual(len(transactions), len(expected_transactions))

        for idx in range(len(transactions)):
            et = expected_transactions[idx]
            t = transactions[idx]

            self.assertEqual(et['date'], t.date)
            self.assertEqual(et['description'], t.description)
            self.assertEqual(et['amount'], t.amount)

    def test_amex_csv_definition_validation_fail(self):
        file_paths = [
            './tests/mocks/bad/amex_activity_bad_example_1.csv',
            './tests/mocks/bad/amex_activity_bad_example_2.csv'
        ]

        for file_path in file_paths:
            result = validate_csv(file_path, amex_csv_definition)
            self.assertEqual(result, False)

    #################################################################################
    #################################################################################
    #################################################################################

    def test_wf_activity_csv_definition_parse(self):
        file_path = './tests/mocks/good/wf_activity_good_example.csv'

        try:
            transactions = parse_csv_to_transactions(file_path, wf_activity_csv_definition)
        except Exception as e:
            self.fail(f"An exception was thrown: {e}")

        self.assertEqual(len(transactions), len(expected_transactions))
        
        for idx in range(len(transactions)):
            et = expected_transactions[idx]
            t = transactions[idx]

            self.assertEqual(et['date'], t.date)
            self.assertEqual(et['description'], t.description)
            self.assertEqual(et['amount'], t.amount)

    def test_wf_activity_csv_definition_validation_fail(self):
        file_paths = [
            './tests/mocks/bad/wf_activity_bad_example_1.csv',
            './tests/mocks/bad/wf_activity_bad_example_2.csv'
        ]

        for file_path in file_paths:
            result = validate_csv(file_path, wf_activity_csv_definition)
            self.assertEqual(result, False)

    #################################################################################
    #################################################################################
    #################################################################################

    def test_wf_spending_report_csv_definition_parse(self):
        file_path = './tests/mocks/good/wf_spending_report_good_example.csv'

        try:
            transactions = parse_csv_to_transactions(file_path, wf_csv_definition)
        except Exception as e:
            self.fail(f"An exception was thrown: {e}")

        self.assertEqual(len(transactions), len(expected_transactions))
        
        for idx in range(len(transactions)):
            et = expected_transactions[idx]
            t = transactions[idx]

            self.assertEqual(et['date'], t.date)
            self.assertEqual(et['description'], t.description)
            self.assertEqual(et['amount'], t.amount)

    def test_wf_activity_csv_definition_validation_fail(self):
        file_paths = [
            './tests/mocks/bad/wf_spending_report_bad_example_1.csv',
            './tests/mocks/bad/wf_spending_report_bad_example_2.csv'
        ]

        for file_path in file_paths:
            result = validate_csv(file_path, wf_csv_definition)
            self.assertEqual(result, False)

    #################################################################################
    #################################################################################
    #################################################################################