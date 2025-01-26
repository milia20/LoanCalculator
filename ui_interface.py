from tkinter import BOTH, LEFT, Button, Entry, Frame, Label, Radiobutton, StringVar, Tk

import matplotlib.backends.backend_tkagg
import matplotlib.pyplot as plt

from Loan import Loan

__author__ = "Ilya"


class LoanCalculatorApp:
    def __init__(self, root):
        self.loan = Loan()
        self.root = root
        self.root.title("Loan Calculator")
        self.root.geometry("800x700")
        self.root.configure(bg="#f7f7f7")

        self.init_ui()

    def init_ui(self):
        # Frames
        self.amount_frame = Frame(self.root, bg="#f7f7f7")
        self.rate_frame = Frame(self.root, bg="#f7f7f7")
        self.term_frame = Frame(self.root, bg="#f7f7f7")
        self.type_frame = Frame(self.root, bg="#f7f7f7")
        self.result_frame = Frame(self.root, bg="#f7f7f7")

        # Widgets
        Label(self.amount_frame, text="Loan Amount:", bg="#f7f7f7", font=("Arial", 12)).pack(side=LEFT, padx=10)
        self.amount_entry = Entry(self.amount_frame, font=("Arial", 12), width=20)
        self.amount_entry.pack(side=LEFT)

        Label(self.rate_frame, text="Interest Rate (%):", bg="#f7f7f7", font=("Arial", 12)).pack(side=LEFT, padx=10)
        self.rate_entry = Entry(self.rate_frame, font=("Arial", 12), width=20)
        self.rate_entry.pack(side=LEFT)

        Label(self.term_frame, text="Loan Term (Months):", bg="#f7f7f7", font=("Arial", 12)).pack(side=LEFT, padx=10)
        self.term_entry = Entry(self.term_frame, font=("Arial", 12), width=20)
        self.term_entry.pack(side=LEFT)

        self.loan_type = StringVar(value="Annuity")
        Radiobutton(
            self.type_frame, text="Annuity", variable=self.loan_type, value="Annuity", bg="#f7f7f7", font=("Arial", 12)
        ).pack(side=LEFT, padx=10)
        Radiobutton(
            self.type_frame,
            text="Differentiated",
            variable=self.loan_type,
            value="Differentiated",
            bg="#f7f7f7",
            font=("Arial", 12),
        ).pack(side=LEFT, padx=10)

        self.calculate_button = Button(
            self.root,
            text="Calculate",
            font=("Arial", 14),
            bg="#0078d7",
            fg="white",
            width=20,
            command=self.calculate_loan,
        )
        self.calculate_button.pack(pady=20)

        self.result_label = Label(self.result_frame, text="", bg="#f7f7f7", font=("Arial", 12))
        self.result_label.pack()

        self.graph_frame = Frame(self.root, bg="#f7f7f7")
        self.fig, self.ax = plt.subplots()
        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(self.fig, master=self.graph_frame)

        # Layout
        self.amount_frame.pack(pady=10)
        self.rate_frame.pack(pady=10)
        self.term_frame.pack(pady=10)
        self.type_frame.pack(pady=10)
        self.result_frame.pack(pady=20)
        self.graph_frame.pack(fill=BOTH, expand=True)
        self.canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    def calculate_loan(self):
        try:
            amount = float(self.amount_entry.get())
            rate = float(self.rate_entry.get())
            term = int(self.term_entry.get())
            loan_type = self.loan_type.get()

            self.loan = Loan(amount, rate, term, loan_type)
            payment_schedule = self.loan.generate_payment_schedule()
            overpayment = self.loan.overpayment([p[1] for p in payment_schedule])

            self.result_label.config(text=f"Total Overpayment: {overpayment:.2f} \u20BD")
            self.display_graph(payment_schedule)

        except ValueError:
            self.result_label.config(text="Invalid input! Please enter numeric values.")

    def display_graph(self, payment_schedule):
        """
        Display the payment schedule graph.
        """
        self.ax.clear()
        months, payments = zip(*payment_schedule)
        self.ax.bar(months, payments, color="#0078d7")
        self.ax.set_title("Payment Schedule", fontsize=14, color="#333333")
        self.ax.set_xlabel("Month", fontsize=12, color="#333333")
        self.ax.set_ylabel("Payment (\u20BD)", fontsize=12, color="#333333")
        self.ax.tick_params(colors="#333333")

        for idx, value in enumerate(payments):
            self.ax.text(idx + 1, value + 10, f"{value:.2f}", ha="center", fontsize=9, color="#333333")

        self.canvas.draw()


if __name__ == "__main__":
    window = Tk()
    app = LoanCalculatorApp(window)
    window.mainloop()
