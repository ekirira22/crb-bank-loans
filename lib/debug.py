#! /usr/bin/env python3
from models.loans import *

import ipdb

# Test data
Bank.drop_table()
Customer.drop_table()
Loan.drop_table()

Bank.create_table()
Customer.create_table()
Loan.create_table()

equity = Bank.create("Equity", "Nyeri")
coop = Bank.create("Coop Bank", "Nairobi")
kcb = Bank.create("KCB Group", "Kwale")

ruth = Customer.create("Ruth", "Gathoni", "ruthyg@gmail.com", 1000000)
alex = Customer.create("Alex", "Maranga", "alex@gmail.com", 2340000)
eric = Customer.create("Eric", "Kirira", "eric@gmail.com", 234000)
larry = Customer.create("Larry", "Mahiu", "larrylance@gmail.com", 45000)

ruth_loan_equity = Loan.create("Mortgage", 200000, equity, ruth)
ruth_loan_coop = Loan.create("Car-Loan", 340000, coop, ruth)
alex_loan_coop = Loan.create("Refinance", 160000, equity, alex)
eric_loan_coop = Loan.create("Biashara", 230000, coop, eric)

larry_loan_kcb_edu = Loan.create("Education-Loan", 15000, kcb, larry)
larry_loan_kcb_car = Loan.create("Car-Loan", 15000, kcb, larry)



ipdb.set_trace()
