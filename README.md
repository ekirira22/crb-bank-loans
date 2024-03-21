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

## Methodology

