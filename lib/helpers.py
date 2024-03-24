# lib/helpers.py
#! /usr/bin/env python3
from models.banks import Bank
from models.customers import Customer
from models.loans import Loan

# Exits Program
def exit_program():
    print("Goodbye!")
    exit()

"""
    BANK HELPERS
"""

# Creates new bank intsance
def create_bank():
    name = input("Enter Bank Name: \n> ")
    branch = input("Enter Bank Branch: \n> ")
    
    try:
        new_bank = Bank.create(name, branch)
        # print success message
        print(f"Added {new_bank.name} bank | {new_bank.branch} branch successfully")  
    except Exception as exc:
        print("Error creating the new bank", exc)


# Fetches and prints all banks
def get_all_banks():
    [print(f"Bank Name: {bank.name} | Bank Branch: {bank.branch}") for bank in Bank.get_all()]


# Fetches and prints bank by name
def find_bank_by_name():
    name = input("Enter existing Bank Name \n> ")
    bank_name = Bank.find_by_name(name)
    print(f"Bank Name: {bank_name.name} | Bank Branch: {bank_name.branch}") if bank_name else print(f"Bank: {name} does not exist!!")


# Fetches and prints bank by ID
def find_bank_by_id():
    id_ = input("Enter existing Bank ID \n> ")
    bank = Bank.find_by_id(id_)
    print(f"Bank Name: {bank.name} | Bank Branch: {bank.branch}") if bank else print(f"Bank with ID: {id_} does not exist!!")


# Fetches and displays all customers belonging to a bank instance
def all_bank_customers():
    id_ = int(input("Enter Bank ID\n> "))
    if bank := Bank.find_by_id(id_):
        customer_ids =  [val.customer_id for val in Loan.get_all() if val.bank_id is bank.id]
        return print(set([Customer.find_by_id(customer_id) for customer_id in customer_ids])) if customer_ids else print("No customers with Loans")
    else:
        print(f"Bank with Bank ID: {id_} not found")


# Fetches and displays all loans belonging to a bank instance
def all_bank_loans():
    id_ = int(input("Enter Bank ID\n> "))
    if bank := Bank.find_by_id(id_):
        loans_ids = [val.id for val in Loan.get_all() if val.bank_id is bank.id]
        return [print(Loan.find_by_id(loan_id)) for loan_id in loans_ids] if loans_ids else print("No disbursed Loans available")
    else:
        print(f"Bank with Bank ID: {id_} not found")


# Updates bank details
def update_bank_details():
    id_ = input("Enter Bank's ID:\n> ")
    if bank := Bank.find_by_id(id_):
        try:
            name = input("Enter the Bank's new name:\n> ")
            bank.name = name
            branch = input("Enter Bank's new branch:\n> ")
            bank.branch = branch

            bank.update()
            print(f"Bank successfuly updated: {bank}")
        except Exception as exc:
            print("Error Updating Bank", exc)
    else:
        print(f"Bank with Bank ID: {id_} not found")


# Delete bank along with loans associated with it
def delete_bank():
    id_ = input("Enter the ID of Bank to delete:\n> ")
    if bank := Bank.find_by_id(id_):
        try:
            bank.delete()
            print(f'Bank ID: {id_} | Bank Name: {bank.name} | Bank Branch: {bank.branch} and associated loans deleted')
        except Exception as exc:
            print("Error deleting bank: ", exc)
    else:
        print(f'Bank {id_} not found')


"""
    CUSTOMER HELPERS
"""


# Creates a new customer
def create_customer():
    first_name = input("Enter Customer First Name: \n> ")
    last_name = input("Enter Customer Last Name: \n> ")
    email = input("Enter Customer Email: \n> ")
    loan_limit_ = int(input("Enter Customer Loan Limit: \n> "))
    
    try:
        new_customer = Customer.create(first_name, last_name, email, loan_limit_)
        # Print out success message
        print(f"Added {new_customer.first_name} {new_customer.last_name} successfully")
    except Exception as exc:
        print("Error creating the new customer", exc)


# Fetches and prints all customers
def get_all_customers():
    [print(f"Name: {customer.first_name} {customer.last_name} | Email: {customer.email} | Loan limit: {customer.loan_limit}") for customer in Customer.get_all()]


# Finds a customer by name
def find_customer_by_name():
    customer_name = input("Enter existing customer first name \n> ")
    customer = Customer.find_by_name(customer_name)
    print(f"Name: {customer.first_name} {customer.last_name} | Email: {customer.email}") if customer else print(f"Customer: {customer_name} does not exist!!")


# Finds a customer by ID
def find_customer_by_id():
    id_ = input("Enter existing Customer ID \n> ")
    customer = Customer.find_by_id(id_)
    print(f"Name: {customer.first_name} {customer.last_name} | Email: {customer.email}") if customer else print(f"Customer with ID: {id_} does not exist!!")


# Returns a list of banks a customer has borrowed a loan from
def all_customer_banks():
    id_ = int(input("Enter Customer's ID\n> "))
    if customer := Customer.find_by_id(id_): 
        print(customer.banks())
    else:
        print(f"Customer with ID: {id_} does not exist")


# Returns a list of loans of the user's instance
def all_customer_loans():
    id_ = int(input("Enter Customer's ID\n> "))
    if customer := Customer.find_by_id(id_):       
        print(customer.all_loans_details())
    else:
        print(f"Customer with ID: {id_} does not exist")


# Returns loans in a Bank instance
def total_customer_bank_loans():
    id_ = int(input("Enter Customer's ID\n> "))
    bank_id_ = int(input("Enter Bank's ID\n> "))
    if customer := Customer.find_by_id(id_):       
        print(customer.bank_loan_total(Bank.find_by_id(bank_id_)))
    else:
        print(f"Customer with ID: {id_} or Bank with ID: {bank_id_} does not exist")


# Returns the total cumulative loan of a user
def loan_total():
    id_ = int(input("Enter Customer's ID\n> "))
    if customer := Customer.find_by_id(id_):
        loan_total = Customer.loan_total(customer)
        print(f"{customer.first_name}'s total Loan is: KES {loan_total}")
    else:
        print(f"Customer with ID: {id_} does not exist")


# Updates the details of a customer instance
def update_customer():
    id_ = int(input("Enter Customer's ID:\n> "))
    if customer := Customer.find_by_id(id_):
        try:
            first_name = input("Enter the Customer's First name:\n> ")
            customer.first_name = first_name
            last_name = input("Enter the Customer's Last name:\n> ")
            customer.last_name = last_name
            email = input("Enter the Customer's Email:\n> ")
            customer.email = email
            loan_limit = int(input("Enter the Customer's Loan Limit:\n> "))
            customer.loan_limit = loan_limit
            customer.update()

            print(f"Customer successfuly updated: {customer}")
        except Exception as exc:
            print("Error Updating Customer", exc)
    else:
        print(f"Customer with Customer ID: {id_} not found")


# Deletes a customer and all their associated loans
def delete_customer():
    id_ = int(input("Enter the ID of Customer to delete:\n> "))
    if customer := Customer.find_by_id(id_):
        try:
            customer.delete()
            print(f'Customer ID: {id_} | Customer Name: {customer.first_name} {customer.last_name} and associated loans deleted')
        except Exception as exc:
            print("Error deleting customer", exc)
    else:
        print(f'Customer with ID: {id_} not found')


# Registers a customer for a Loan
def register_loan():
    id_ = int(input("Enter the ID of Customer to Register Loan:\n> "))
    bank_id_ = int(input("Enter the ID of Bank to Register Loan:\n> "))
    loan_type = input("Enter the Loan Type Category:\n> ")
    loan_amount = int(input("Enter the Loan Amount in KES:\n> "))
    if customer := Customer.find_by_id(id_):
        try:
            if not isinstance(customer, Customer):
                raise TypeError("customer argument must be of type Customer")
            Loan.create(loan_type, loan_amount, Bank.find_by_id(bank_id_), customer)
        except Exception as exc:
            print("Error processing Loan", exc)
    else:
        print(f'Customer with ID: {id_} not found')


# Settles Loan for a customer. Credits the excess to customer account
def settle_loan():
    id_ = int(input("Enter the ID of Customer to Settle Loan:\n> "))
    bank_id_ = int(input("Enter the ID of Bank to Settle Loan:\n> "))
    loan_type = input("Enter the Loan Type Category:\n> ")
    loan_amount = int(input("Enter the Loan Amount in KES:\n> "))
    if customer := Customer.find_by_id(id_):
        try:
            customer.pay_loan(loan_type, Bank.find_by_id(bank_id_), loan_amount)
        except Exception as exc:
            print("Error Settling Loan. Check Bank ID or Cust ID >> ", exc)
    else:
        print(f'Customer with ID: {id_} not found')
