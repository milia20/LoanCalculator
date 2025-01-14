import math


class Loan:
    """
    A class to represent a loan and perform calculations for annuity and differentiated payments.

    Attributes:
        amount (int): The principal loan amount.
        annual_percent_rate (float): The annual interest rate as a percentage.
        month (int): The loan term in months.
        loan_type (str): The type of loan ("Annuity" or "Differentiated").
    """

    def __init__(self, amount: int = 0, percent: float = 0.0, month: int = 0, loan_type: str = "Annuity") -> None:
        self.amount: int = amount
        self.annual_percent_rate: float = percent
        self.annual_interest_rate: float = self.annual_percent_rate / 100
        self.monthly_interest_rate: float = self.annual_interest_rate / 12
        self.month: int = month
        self.loan_type: str = loan_type

    def set_interest_rate(self, percent: float) -> None:
        """Set a new annual interest rate."""
        self.annual_percent_rate = percent
        self.annual_interest_rate = self.annual_percent_rate / 100
        self.monthly_interest_rate = self.annual_interest_rate / 12

    def set_loan_type(self, loan_type: str) -> None:
        """Set the type of loan."""
        self.loan_type = loan_type

    def overpayment(self, payments: list) -> float:
        """
        Calculate the overpayment made for the loan.

        Args:
            payments (list): A list of monthly payments.

        Returns:
            float: The total overpayment.
        """
        return round(sum(payments) - self.amount, 2)

    def number_payments_annuity(self, month_payment) -> int:
        """
        Calculate the number of monthly annuity payments.
        :param month_payment: your payment for 1 month
        :return: number months for this payment
        """
        n = math.log(
            month_payment / (month_payment - self.monthly_interest_rate * self.amount), 1 + self.monthly_interest_rate
        )
        return math.ceil(n)

    def loan_principal_annuity(self, month_payment) -> float:
        """
        Calculate the loan principal amount for an annuity payment.
        :param month_payment: your payment for 1 month
        :return: amount of credit after finish repayment
        """
        amount = month_payment / (
            (self.monthly_interest_rate * (1 + self.monthly_interest_rate) ** self.month)
            / ((1 + self.monthly_interest_rate) ** self.month - 1)
        )
        return amount

    def payment_annuity_pure(self) -> float:
        """
        Calculate the exact monthly annuity payment.

        Returns:
            float: The monthly annuity payment.
        """
        return self.amount * (
            (self.monthly_interest_rate * (1 + self.monthly_interest_rate) ** self.month)
            / ((1 + self.monthly_interest_rate) ** self.month - 1)
        )

    def payment_annuity_ceil(self) -> int:
        """
        Calculate the monthly annuity payment rounded up to the nearest integer.

        Returns:
            int: The rounded annuity payment.
        """
        return math.ceil(self.payment_annuity_pure())

    def payment_differentiated_pure(self, m: int) -> float:
        """
        Differentiated payments float
        :param m: Payment month number m >= 1
        :return: Payment for m month
        :rtype: float
        """
        # every month new
        # m => 1
        diff_payment = self.amount / self.month + self.monthly_interest_rate * (
            self.amount - ((self.amount * (m - 1)) / self.month)
        )
        return diff_payment

    def payment_differentiated_ceil(self, stay_pay: float) -> float:
        """
        Differentiated payments ceil, overpayment goes into reducing the last payment
        :param stay_pay: The remaining amount of debt
        :return: Payment for next month
        :rtype: int
        """
        # every month new
        diff_payment = self.amount / self.month + self.monthly_interest_rate * stay_pay
        if diff_payment > stay_pay:
            return stay_pay
        return diff_payment

    def calculate_payment_ceil(self) -> list:
        """
        Calculating all payments ceil
        :return: payments
        """
        payment: list = []

        if self.loan_type[0] == "A":
            payment = [self.payment_annuity_ceil()] * self.month

        else:
            stay_pay = self.amount
            for _ in range(self.month):
                diff = self.payment_differentiated_ceil(stay_pay)
                ceil_diff = math.ceil(diff)
                stay_pay -= (ceil_diff - diff) + self.amount / self.month
                payment.append(ceil_diff)

        return payment

    def calculate_payment_pure(self) -> list:
        """
        Calculating all payments
        :return: payments
        """
        payment: list = []
        # accuracy of 2 decimal places
        if self.loan_type[0] == "A":
            payment = [round(self.payment_annuity_pure(), 2)] * self.month

        else:
            for month_now in range(1, self.month + 1):
                payment.append(round(self.payment_differentiated_pure(month_now), 2))

        return payment
