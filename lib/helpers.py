# lib/helpers.py
#! /usr/bin/env python3
from models.loans import *

import re
import random

# Exits Program
def exit_program():
    print("Goodbye!")
    exit()

# Creates new bank intsance
def create_bank():
    name = input("Enter Bank Name: \n")
    branch = input("Enter Bank Branch: \n")
    
    try:
        new_bank = Bank.create(name, branch)
        # print success message
        print(f"Added {new_bank.name} bank | {new_bank.branch} branch successfully")  
    except Exception as exc:
        print("Error creating the new bank", exc)

# Fetches and prints all banks
def get_all_banks():
    [print(f"Bank Name: {bank.name} | Bank Branch: {bank.branch}") for bank in Bank.get_all()]


# Regex pattern for validating email -> Returns False if pattern is not fulfilled 
def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

def limit_bonus():
    return random.randint(5000, 20000)