# lib/main.py
#! /usr/bin/env python3
from models.initialize import CURSOR, CONN
from models.loans import *

from helpers import (
    exit_program,
    create_bank
)


def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            bank_name = input("Enter Bank Name: \n")
            bank_branch = input("Enter Bank Branch: \n")
            new_bank = create_bank(bank_name, bank_branch)
        elif choice == "2":
            all_banks = Bank.get_all()
            [print(f"Bank Name: {bank.name} | Bank Branch: {bank.branch}") for bank in all_banks]            
        else:
            print("Invalid choice")


def menu():
    print("====================================================")
    print("Please select an option:")
    print("0. Exit the program")
    print("1. Create a New Bank")
    print("2. List all Accredited Banks")
    print("====================================================")




if __name__ == "__main__":
    main()
