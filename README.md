# Phase 3 CLI+ORM Final Project 

## CRB Bank Loan Manager

- Track the number of loans a bank has
- Track the number of loans a customer has

---

## Introduction

The CRB loan bank manager is a database that keeps track of all banks loaning customers money and all customers that have loans in various bank. 

The relationship between the banks and customers is a many-many relationship. We will have another table called loans that will act as the contract table to the banks and customers.

1. A Bank can have many customers and many customers can belong to a bank

    |Bank| * ...............* |Customer|

2. A bank can have many loans belonging to various customers and a loan can only belong to one bank

    |Bank| 1 ...............* |Loans|

3. A customer can have many loans belonging to various banks and a loan can only belong to one customer

    |Customers| 1 ................* |Bank|

### TABLE SCHEMA

| Bank ||
| ----------- | ----------- |
| id | INT |
| name | TEXT|


| Customers ||
| ----------- | ----------- |
| id | INT |
| first_name | TEXT|
| last_name | TEXT|
| mobile | INT|


| Loans ||
| ----------- | ----------- |
| id | INT |
| loan_type | TEXT|
| amount | INT|
| bank_id | INT - FK|
| customer_id | INT - FK|

## User Stories

CS. Njuguna Ndegwa wants to see how many Kenyans have Loans and in which banks. 
The following are the various functions that a user can be allowed to use.

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


## Set up and How to Run

1. Download the git folder and run debug.py to load seed data into the database

2. Ensure you are in a python environment. Install any additional dependencies you know you'll need for your project by adding them to the Pipfile. Then run the commands:
    `pipenv install`
    `pipenv shell`

3. Run the main.py file using `python 3 main.py`
4. Execute the various functions using the CRB Menu provided