from tkinter import *

import matplotlib.backends.backend_tkagg
import matplotlib.pyplot as plt

from Loan import Loan

__author__ = 'Ilya'


def make_graph(my_payment):
    ax.clear()
    print(my_payment)
    ax.bar([_ for _ in range(1, len(my_payment) + 1)], my_payment)
    ax.set_xlabel("Месяца")
    ax.set_ylabel("Выплата руб")
    ax.set_title("График выплат")
    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.2f'),
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center',
                    xytext=(0, -12),
                    textcoords='offset points')

    graph.draw()


def calculate_result(my_loan):
    my_loan.set_interest_rate(int(text_interest_rate.get()))
    my_loan.month = int(text_mount.get())
    my_loan.amount = int(text_amount.get())
    if loan_bool.get():
        my_loan.loan_type = 'Annuity'
    else:
        my_loan.loan_type = 'Differentiated'

    pay = my_loan.calculate_payment_pure()
    over = my_loan.overpayment(pay)
    overpay.set(f"Переплата {over} р")
    make_graph(pay)


user_loan = Loan(0, 0, 0, "Annuity")

# Window settings
window = Tk()
window.title("Loan calculator")
# window.resizable(width=False, height=False)
window.geometry("800x700")

amount_frame = Frame(window)
interest_rate_frame = Frame(window)
mount_frame = Frame(window)
loan_type_frame = Frame(window)

# Event
btn = Button(window, width=10, height=2, text="Рассчитать", bg="white", fg="black",
             command=lambda: calculate_result(user_loan))
fig, ax = plt.subplots()

graph = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=window)

amount = Label(amount_frame, text="Сумма долга")
interest_rate = Label(interest_rate_frame, text="%")
mount = Label(mount_frame, text="Месяца")
overpay = StringVar()
overpay.set("Переплата 0 р")
payment = Label(window, textvariable=overpay)

text_amount = Entry(amount_frame)
text_interest_rate = Entry(interest_rate_frame)
text_mount = Entry(mount_frame)

loan_bool = BooleanVar()
loan_bool.set(True)
Annuity_btn = Radiobutton(loan_type_frame, text='Annuity', variable=loan_bool, value=True)
Differentiated_btn = Radiobutton(loan_type_frame, text='Differentiated', variable=loan_bool,
                                 value=False)
# Packer

graph.get_tk_widget().pack(fill=BOTH, expand=True)
payment.pack()

amount_frame.pack()
interest_rate_frame.pack()
mount_frame.pack()
loan_type_frame.pack()

amount.pack(side=LEFT, padx=39)
text_amount.pack(side=LEFT, padx=39)

interest_rate.pack(side=LEFT, padx=70)
text_interest_rate.pack(side=LEFT, padx=70)

mount.pack(side=LEFT, padx=54)
text_mount.pack(side=RIGHT, padx=54)

Annuity_btn.pack(side=LEFT)
Differentiated_btn.pack(side=LEFT)

btn.pack()

window.mainloop()
