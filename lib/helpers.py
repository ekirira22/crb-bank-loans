# lib/helpers.py
#! /usr/bin/env python3
from models.banks import Bank
from models.customers import Customer

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

# Fetches and displays all customers belonging to a certain bank
def all_bank_customers():
    id_ = input("Enter Bank ID\n> ")
    if bank := Bank.customers(Bank.find_by_id(id_)):
        print(bank)
    else:
        print(f"Bank with Bank ID: {id_} not found")

# Fetches and displays all loans belonging to a certain bank
def all_bank_loans():
    id_ = input("Enter Bank ID\n> ")
    if bank := Bank.loans(Bank.find_by_id(id_)):
        print(bank)
    else:
        print(f"Bank with Bank ID: {id_} not found")

# Update bank details
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

# Delete bank
def delete_bank():
    id_ = input("Enter the ID of Bank to delete:\n> ")
    if bank := Bank.find_by_id(id_):
        bank.delete()
        print(f'Bank ID: {id_} | Bank Name: {bank.name} | Bank Branch: {bank.branch} and associated loans deleted')
    else:
        print(f'Department {id_} not found')


"""
    CUSTOMER HELPERS
"""

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

def get_all_customers():
    [print(f"Name: {customer.first_name} {customer.last_name} | Email: {customer.email} | Loan limit: {customer.loan_limit}") for customer in Customer.get_all()]

def find_customer_by_name():
    customer_name = input("Enter existing customer first name \n> ")
    customer = Customer.find_by_name(customer_name)
    print(f"Name: {customer.first_name} {customer.last_name} | Email: {customer.email}") if customer else print(f"Customer: {customer_name} does not exist!!")

def find_customer_by_id():
    id_ = input("Enter existing Customer ID \n> ")
    customer = Customer.find_by_id(id_)
    print(f"Name: {customer.first_name} {customer.last_name} | Email: {customer.email}") if customer else print(f"Customer with ID: {id_} does not exist!!")

def all_customer_loans():
    id_ = int(input("Enter Customer's ID\n> "))
    customer = Customer.find_by_id(id_)
    return customer.loans()

def loan_total():
    id_ = int(input("Enter Customer's ID\n> "))

    customer = Customer.find_by_id(id_)
    loan_total = Customer.loan_total(customer)
    return f"{customer.first_name}'s total Loan is: KES {loan_total}"

