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
        for params in self.test_params:
            amount, percent, months, loan_type, expected_pure, _, _, _ = params
            loan = Loan(amount, percent, months, loan_type)
            result = loan.calculate_payment_pure()
            self.assertEqual(result, expected_pure, f"Failed on pure payment calculation for {loan_type}")

    def test_calculate_payment_ceil(self):
        for params in self.test_params:
            amount, percent, months, loan_type, _, expected_ceil, _, _ = params
            loan = Loan(amount, percent, months, loan_type)
            result = loan.calculate_payment_ceil()
            self.assertEqual(result, expected_ceil, f"Failed on ceil payment calculation for {loan_type}")

    def test_overpayment_pure(self):
        for params in self.test_params:
            amount, percent, months, loan_type, expected_pure, _, expected_overpayment, _ = params
            loan = Loan(amount, percent, months, loan_type)
            result = loan.overpayment(expected_pure)
            self.assertAlmostEqual(
                result, expected_overpayment, places=2, msg=f"Failed on pure overpayment calculation for {loan_type}"
            )

    def test_overpayment_ceil(self):
        for params in self.test_params:
            amount, percent, months, loan_type, _, expected_ceil, _, expected_overpayment = params
            loan = Loan(amount, percent, months, loan_type)
            result = loan.overpayment(expected_ceil)
            self.assertAlmostEqual(
                result, expected_overpayment, places=2, msg=f"Failed on ceil overpayment calculation for {loan_type}"
            )

    def test_additional_methods(self):
        loan = Loan(10000, 10, 12, "Annuity")
        annuity_payment = loan.payment_annuity_pure()

        # Test loan principal calculation
        principal = loan.loan_principal_annuity(annuity_payment)
        self.assertAlmostEqual(principal, 10000, places=2, msg="Failed on loan principal calculation")

        # Test number of payments calculation
        num_payments = loan.number_payments_annuity(annuity_payment)
        self.assertEqual(num_payments, 12, "Failed on number of payments calculation")
