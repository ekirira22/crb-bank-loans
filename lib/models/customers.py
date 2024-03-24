#! /usr/bin/env python3
from models.initialize import CURSOR, CONN
import random
import re

class Customer:

    all = {}

    def __init__(self, first_name, last_name, email, loan_limit, id=None) -> None:
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.loan_limit = loan_limit

    # Returns details of instance
    def __repr__(self) -> str:
        return f"<Customer {self.id}: {self.first_name} | {self.last_name} | {self.email} | {self.loan_limit}>"
    

    """
        PROPERTY METHODS
    """
    

    @property
    def first_name(self):
        return self._first_name
    @first_name.setter
    def first_name(self, first_name):
        if isinstance(first_name, str) and len(first_name) > 0:
            self._first_name = first_name
            return
        raise TypeError("Customer first name has to be a string and cannot be empty")
    

    @property
    def last_name(self):
        return self._last_name
    @last_name.setter
    def last_name(self, last_name):
        if isinstance(last_name, str) and len(last_name) > 0:
            self._last_name = last_name
            return
        raise TypeError("Customer last name has to be a string and cannot be empty")
    

    @property
    def email(self):
        return self._email
    @email.setter
    def email(self, email):
        if isinstance(email, str) and validate_email(email):
            self._email = email
            return
        raise TypeError("Customer email has to be a valid email")
    

    @property
    def loan_limit(self):
        return self._loan_limit
    @loan_limit.setter
    def loan_limit(self, loan_limit):
        if not isinstance(loan_limit, int) and loan_limit > 0:
            raise TypeError("Loan Limit has to be a number and cannot be less than zero")
        self._loan_limit = loan_limit


    """
        ORM CLASS METHODS
    """


    @classmethod
    def create_table(cls) -> None:
        # Create a new table to persist the attributes of Customer instances
        sql = """
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                email TEXT,
                loan_limit INTEGER
            )
        """
        CURSOR.execute(sql)
        CONN.commit()


    @classmethod
    def drop_table(cls) -> None:
        # Drop the table to persist the attributes of Customer instances
        sql = """
            DROP TABLE IF EXISTS customers;
        """
        CURSOR.execute(sql)
        CONN.commit()


    @classmethod
    def create(cls, first_name, last_name, email, loan_limit):
        new_Customer = cls(first_name, last_name, email, loan_limit)
        new_Customer.save()
        return new_Customer
    

    @classmethod
    def instance_from_db(cls, result):
        # first check if it exists in all dict
        if customer := cls.all.get(result[0]):
            # Reset values incase of any alteration
            customer.first_name = result[1]
            customer.last_name = result[2]
            customer.email = result[3]
            customer.loan_limit = result[4]
        else:
            # not in dictionary but in db
            customer = cls(result[1], result[2], result[3], result[4])
            customer.id = result[0]
            cls.all[customer.id] = customer
        return customer
    

    @classmethod
    def get_all(cls):
        # Return a list containing a Customer object per row in the table
        sql = """
            SELECT * FROM customers
        """
        results = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(result) for result in results]
    

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM customers WHERE id = ?
        """
        result = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(result) if result else None
    

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * FROM customers WHERE first_name = ?
        """
        result = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(result) if result else None

    
    """
        ORM CRUD INSTANCE METHODS
    """


    def save(self) -> None:
        # Insert a new row with the first_name, last_name aned email values of the current Customer instance. 
        # Update object id attribute using the primary key value of new row.

        sql = """
            INSERT INTO customers (first_name, last_name, email, loan_limit) VALUES (?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.first_name, self.last_name, self.email, self.loan_limit))
        CONN.commit()

        # Now store the ID
        self.id = CURSOR.lastrowid

        # Save this Customer instance in a dictionary with id as the key
        type(self).all[self.id] = self


    def update(self):
        # Update the table row corresponding to the current Customer instance.
        sql = """
            UPDATE customers SET first_name = ?, last_name = ?, email = ?, loan_limit = ? WHERE id = ?
        """
        CURSOR.execute(sql, (self.first_name, self.last_name, self.email, self.loan_limit, self.id))
        CONN.commit()
        print(f"Customer details successfuly updated >>\n {self.first_name} | {self.last_name} | {self.email} | {self.loan_limit} ")


    def delete(self):
        from models.loans import Loan
        # Deletes by Association - delete all customers who have loans associated to this instance
        # before deleting the bank itself

        loans_delete_ids = [loan.id for loan in Loan.get_all() if loan.customer_id is self.id]
        [Loan.delete_by_id(id) for id in loans_delete_ids]
       
        # Delete the table row corresponding to the current Customer instance
        sql = """
            DELETE FROM customers WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        print("Customer and associated loans successfuly deleted")

        # Delete from all and set id to None
        del type(self).all[self.id]
        self.id = None

        
    """
        ORM ASSOCIATION METHODS
    """


    # Returns a list of banks a customer has borrowed a loan from
    def banks(self):
        from models.banks import Bank
        from models.loans import Loan
        bank_ids =  [val.bank_id for val in Loan.get_all() if val.customer_id is self.id]
        return set([Bank.find_by_id(bank_id) for bank_id in bank_ids]) if bank_ids else print("No Bank with Loan")


    # Returns a list of loans of the user's instance
    def loans(self):
        from models.loans import Loan
        loans_ids = [val.id for val in Loan.get_all() if val.customer_id is self.id]
        return [Loan.find_by_id(loan_id) for loan_id in loans_ids] if loans_ids else print("No Existing Loans")
    

    # Returns the total loan of a user
    def loan_total(self):
        # Returns total of loan
        return sum([loan.loan_amount for loan in self.loans() if loan.customer_id is self.id]) if isinstance(self.loans(), list) else 0
    

    # Returns the loan total a user has in a specific bank
    def bank_loan_total(self, bank):
        from models.banks import Bank

        if isinstance(bank, Bank):
            # Returns total of loan
            return f"{self.first_name}'s outstanding Loan balance in {bank.name} is: KES {sum([loan.loan_amount for loan in self.loans() if loan.customer_id is self.id and loan.bank_id is bank.id])}"
        raise TypeError("Argument passed must an instance of Bank class")
    

    # Customer Pays Loan Function
    def pay_loan(self, loan_type, bank, amount):
        from models.loans import Loan
        from models.loans import Bank
        if not isinstance(bank, Bank):
            raise TypeError("Bank argument should be of class Bank")
        
        current_loan = [loan for loan in self.loans() if loan.bank_id is bank.id and loan.loan_type == loan_type]

        # update loan instance and database
        current_loan[0].loan_amount -= amount
        current_loan[0].update()

        # if loan is zero. Delete loan instance | Give user an extra bonus limit
        if current_loan[0].loan_amount <= 0:
            print(f"Thank you for fully paying you loan") if current_loan[0].loan_amount >= 0 else print(f"Thank you for fully paying you loan. \nExcess of KES {-current_loan[0].loan_amount} has been credited to your account")
            Loan.delete(current_loan[0])

        # increase customers instance and database
        self.loan_limit += amount + limit_bonus()
        self.update()


    # Display all Loan Details
    def all_loans_details(self):
        from models.banks import Bank
        all_loans = self.loans()
        if all_loans:
            for loan in self.loans():
                print(f"Bank: {Bank.find_by_id(loan.bank_id).name} | Loan Type: {loan.loan_type} | Loan Amount: {loan.loan_amount}")
        else:
            print("Customer has no outstanding Loans")




# Regex pattern for validating email -> Returns False if pattern is not fulfilled 
def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None


# get random loan limit bonus
def limit_bonus():
    return random.randint(5000, 20000)
    




