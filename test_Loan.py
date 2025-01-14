from unittest import TestCase

from Loan import Loan


class TestLoan(TestCase):
    def setUp(self):
        self.test_params = [
            # Format:
            # (amount, percent, months, type, expected pure payments, expected ceil payments, pure overpayment, ceil overpayment)
            (10000, 10, 2, "Annuity", [5062.59, 5062.59], [5063, 5063], 125.18, 126),
            (1000, 1, 2, "Differentiated", [500.83, 500.42], [501, 500], 1.25, 1),
        ]

    def test_calculate_payment_pure(self):
        result = self.loan.calculate_payment_pure()
        self.assertEqual(result, self.test_param[self.i][1])

    def test_calculate_payment_ceil(self):
        result = self.loan.calculate_payment_ceil()
        self.assertEqual(result, self.test_param[self.i][2])

    def test_overpayment_pure(self):
        result = self.loan.overpayment(self.loan.calculate_payment_pure())
        self.assertEqual(result, self.test_param[self.i][3])

    def test_overpayment_ceil(self):
        result = self.loan.overpayment(self.loan.calculate_payment_ceil())
        self.assertEqual(result, self.test_param[self.i][4])
