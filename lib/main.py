# lib/main.py
#! /usr/bin/env python3
from models.initialize import CURSOR, CONN
from models.loans import *

from helpers import *


def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            create_bank()
        elif choice == "2":
            get_all_banks()            
        else:
            print("Invalid choice")


def menu():
    print("\n\n====================================================")
    print("----------------------")
    print("|     BANK CLI       |")
    print("----------------------")
    print("Please select an option:")
    print("0. Exit the program")
    print("1. Create a New Bank")
    print("2. List all Accredited Banks")
    print("3. Find Bank by Name")
    print("4. Find Bank by ID")
    print("5. List all Customers in a Bank")
    print("6. List all Loans in a Bank")
    print("7. Update Bank details")
    print("8. Delete Bank")
    print("9. Offer Loan to a Customer")
    print("10. Pay Loan for a Customer")


    
    print("----------------------")
    print("|  CUSTOMER CLI      |")
    print("----------------------")   
    print("11. Create a New Customer")
    print("12. List all Approved Customers")
    print("13. Find Customer by Name")
    print("14. Find Customer by ID")
    print("15. List all Banks a Customer has a borrowed a Loan")
    print("16. List all Loans belonging to a Customer")
    print("17. List all Loans a Customer has in a Bank")
    print("18. List total amount of Loans")
    print("19. List total amount of Loans in a Bank")
    print("20. Update Customer details")
    print("21. Delete Customer")
    print("22. Take a Loan")
    print("23. Pay a Loan")     
    print("====================================================\n\n")




if __name__ == "__main__":
    main()
