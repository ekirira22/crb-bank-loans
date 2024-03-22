# lib/helpers.py
#! /usr/bin/env python3
from models.loans import *

import re
import random

def exit_program():
    print("Goodbye!")
    exit()

def create_bank(name, branch):
    new_bank = Bank.create(name, branch)
    return new_bank


# Regex pattern for validating email -> Returns False if pattern is not fulfilled 
def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

def limit_bonus():
    return random.randint(5000, 20000)