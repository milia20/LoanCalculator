from unittest import TestCase
from Loan import Loan
import random


class TestLoan(TestCase):
    test_param = (((10000, 10, 2, "Annuity"), [5062.59, 5062.59], [5063, 5063], 125.18, 126),
                  # ((10000, 10, 2, "Annuity"), [5062.59, 5062.59], [5063, 5063], 125.18, 126),
                  ((1000, 1, 2, "Differentiated"), [500.83, 500.42], [501, 500], 1.25, 1)
                  )
    i = random.randint(0, len(test_param) - 1)

    def setUp(self):
        self.loan = Loan(self.test_param[self.i][0][0], self.test_param[self.i][0][1],
                         self.test_param[self.i][0][2], self.test_param[self.i][0][3])

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
