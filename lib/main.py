# lib/main.py
#! /usr/bin/env python3
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
        elif choice == "3":
            find_bank_by_name()
        elif choice == "4":
            find_bank_by_id()
        elif choice == "5":
            all_bank_customers()
        elif choice == "6":
            all_bank_loans()
        elif choice == "7":
            update_bank_details()
        elif choice == "8":
            delete_bank()
        elif choice == "9":
            create_customer()
        elif choice == "10":
            get_all_customers()
        elif choice == "11":
            find_customer_by_name()
        elif choice == "12":
            find_customer_by_id()
        elif choice == "13":
            all_customer_banks()
        elif choice == "14":
            all_customer_loans()
        elif choice == "15":
            total_customer_bank_loans()
        elif choice == "16":
            loan_total()
        elif choice == "17":
            update_customer()
        elif choice == "18":
            delete_customer()
        elif choice == "19":
            register_loan()
        elif choice == "20":
            settle_loan()
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
 
    
    print("----------------------")
    print("|  CUSTOMER CLI      |")
    print("----------------------")   
    print("9. Create a New Customer")
    print("10. List all Approved Customers")
    print("11. Find Customer by Name")
    print("12. Find Customer by ID")
    print("13. List all Banks a Customer has a borrowed a Loan")
    print("14. List all Loans belonging to a Customer")
    print("15. List total Loan amount in a Bank")
    print("16. List cumulative total in Loans")
    print("17. Update Customer details")
    print("18. Delete Customer")
    print("19. Register New Loan")
    print("20. Settle Loan")     
    print("====================================================\n\n")




if __name__ == "__main__":
    main()
