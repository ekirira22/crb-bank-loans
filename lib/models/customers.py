#! /usr/bin/env python3
from models.initialize import CURSOR, CONN
from helpers import validate_email

class Customer:

    all = {}

    def __init__(self, first_name, last_name, email, id=None) -> None:
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    # Returns details of instance
    def __repr__(self) -> str:
        return f"<Customer {self.id}: {self.first_name} | {self.last_name} | {self.email}>"
    
    """
        PROPERTY METHODS
    """
    @property
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, first_name):
        if isinstance(first_name, str) and len(first_name) > 1:
            self._first_name = first_name
            return
        raise TypeError("Customer first name has to be a valid name")
    
    @property
    def last_name(self):
        return self._last_name
    
    @last_name.setter
    def last_name(self, last_name):
        if isinstance(last_name, str) and len(last_name) > 1:
            self._last_name = last_name
            return
        raise TypeError("Customer last name has to be a valid name")
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, email):
        if isinstance(email, str) and validate_email(email):
            self._email = email
            return
        raise TypeError("Customer email has to be a valid email")
    
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
                email TEXT
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
    def create(cls, first_name, last_name, email):
        new_Customer = cls(first_name, last_name, email)
        new_Customer.save()
        return new_Customer
    
    @classmethod
    def instance_from_db(cls, result):
        # first check if it exists in all dict
        customer = cls.all.get(result[0])
        if customer:
            # Reset values incase of any alteration
            customer.first_name = result[1]
            customer.last_name = result[2]
            customer.email = result[3]
        else:
            # not in dictionary but in db
            customer = cls(result[1], result[2], result[3])
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

    
    """
        ORM CRUD INSTANCE METHODS
    """

    def save(self) -> None:
        # Insert a new row with the first_name, last_name aned email values of the current Customer instance. 
        # Update object id attribute using the primary key value of new row.

        sql = """
            INSERT INTO customers (first_name, last_name, email) VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (self.first_name, self.last_name, self.email))
        CONN.commit()

        # Now store the ID
        self.id = CURSOR.lastrowid

        # Save this Customer instance in a dictionary with id as the key
        type(self).all[self.id] = self
        # Print out success message

        print(f"Added {self.first_name} {self.last_name} successfully")
        

    def update(self):
        # Update the table row corresponding to the current Customer instance.
        sql = """
            UPDATE customers SET first_name = ?, last_name = ?, email = ? WHERE id = ?
        """
        CURSOR.execute(sql, (self.first_name, self.last_name, self.email, self.id))
        CONN.commit()
        print(f"Customer details successfuly updated >>\n {self.first_name} | {self.last_name} | {self.email} ")


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
        from models.loans import Loan
        from models.banks import Bank

        bank_ids =  [val.bank_id for key, val in Loan.all.items() if val.customer_id is self.id]
        return [Bank.find_by_id(bank_id) for bank_id in bank_ids] if bank_ids else print("No Bank with Loan")
    
    # Returns a list of loans of the user's instance
    def loans(self):
        from models.loans import Loan        
        loans_ids = [val.id for key, val in Loan.all.items() if val.customer_id is self.id]
        return [Loan.find_by_id(loan_id) for loan_id in loans_ids] if loans_ids else print("No Existing Loans")
    
    # Returns the loan total a user has in a specific bank
    def bank_loan_total(self, bank):
        from models.banks import Bank

        if isinstance(bank, Bank):
            # Returns total of loan
            return f"{self.first_name}'s outstanding Loan balance in {bank.name} is: KES {sum([loan.loan_amount for loan in self.loans() if loan.customer_id is self.id and loan.bank_id is bank.id])}"
        raise TypeError("Argument passed must an instance of Bank class")

    




