#! /usr/bin/env python3
from models.initialize import CURSOR, CONN
from models.banks import Bank
from models.customers import Customer

class Loan:

    all = {}

    def __init__(self, loan_type, loan_amount, bank_id, customer_id, id=None) -> None:
        self.id = id
        self.loan_type = loan_type
        self.loan_amount = loan_amount
        self.bank_id = bank_id
        self.customer_id = customer_id

    # Returns details of instance
    def __repr__(self) -> str:
        return f"<Loan {self.id}: {self.loan_type} | {self.bank_id} | {self.customer_id}>"
    
    """
        PROPERTY METHODS
    """
    @property
    def loan_type(self):
        return self._loan_type
    
    @loan_type.setter
    def loan_type(self, loan_type):
        if isinstance(loan_type, str) and len(loan_type) > 1:
            self._loan_type = loan_type
            return
        raise TypeError("Loan type has to be a valid name")
    
    @property
    def loan_amount(self):
        return self._loan_amount
    
    @loan_amount.setter
    def loan_amount(self, loan_amount):
        if isinstance(loan_amount, int or float):
            self._loan_amount = loan_amount
            return
        raise TypeError("Loan amount has to be a number and greater than zero")
    
    """
        ORM CLASS METHODS
    """
    @classmethod
    def create_table(cls) -> None:
        # Create a new table to persist the attributes of Loan instances
        sql = """
            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY,
                loan_type TEXT,
                loan_amount INTEGER,
                bank_id INTEGER,
                customer_id INTEGER,
                FOREIGN KEY(bank_id) REFERENCES banks(id),
                FOREIGN KEY(customer_id) REFERENCES customers(id)
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls) -> None:
        # Drop the table to persist the attributes of Loan instances
        sql = """
            DROP TABLE IF EXISTS loans;
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def create(cls, loan_type, loan_amount, bank, customer):
        # Check if bank and customers and instances
        if isinstance(bank, Bank) and isinstance(customer, Customer):
            # check if the customer has existed their loan limit
            if loan_amount < customer.loan_limit:
                new_loan = cls(loan_type, loan_amount, bank.id, customer.id)
                new_loan.save()
                # update customers loan limit
                customer.loan_limit -= loan_amount
                customer.update()

                return new_loan
            else:
                print(f"Loan limit exceeded. Current Loan: KES {customer.loan_total()} \nKES {loan_amount} borrowed while limit is KES {customer.loan_limit}.\nPay to increase Loan Limit")
                return
        raise TypeError("bank and customer arguments have to be of class Bank and Customer respectively")
    
    @classmethod
    def instance_from_db(cls, result):
        # first check if it exists in all dict
        loan = cls.all.get(result[0])
        if loan:
            # Reset values incase of any alteration
            loan.loan_type = result[1]
            loan.loan_amount = result[2]
            loan.bank_id = result[3]
            loan.customer_id = result[4]
        else:
            # not in dictionary but in db
            loan = cls(result[1], result[2], result[3], result[4])
            loan.id = result[0]
            cls.all[loan.id] = loan
        return loan
    
    @classmethod
    def get_all(cls):
        # Return a list containing a Loan object per row in the table
        sql = """
            SELECT * FROM loans
        """
        results = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(result) for result in results]
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM loans WHERE id = ?
        """
        result = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(result) if result else None
    
    @classmethod
    def delete_by_id(cls, id):
       
        # Get the instance of the id
        loan_to_delete = cls.all.get(id)
        # Delete from all dict
        cls.delete(loan_to_delete)
    
    """
        ORM CRUD INSTANCE METHODS
    """

    def save(self) -> None:
        # Insert a new row with the name and branch values of the current Loan instance. 
        # Update object id attribute using the primary key value of new row.

        sql = """
            INSERT INTO loans (loan_type, loan_amount, bank_id, customer_id) VALUES (?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.loan_type, self.loan_amount, self.bank_id, self.customer_id))
        CONN.commit()

        # Now store the ID
        self.id = CURSOR.lastrowid

        # Save this Loan instance in a dictionary with id as the key
        type(self).all[self.id] = self

        # output result
        print(f"Added {self.loan_type} Loan | Amount: {self.loan_amount} | Bank: {self.bank_id} | Customer: {self.customer_id}")


    def update(self):
        # Update the table row corresponding to the current Loan instance.
        sql = """
            UPDATE loans SET loan_type = ?, loan_amount = ?, bank_id = ?, customer_id = ? WHERE id = ?
        """
        CURSOR.execute(sql, (self.loan_type, self.loan_amount, self.bank_id, self.customer_id, self.id))
        CONN.commit()
        print("Loan successfuly updated")

    def delete(self):
        # Delete the table row corresponding to the current Loan instance
        sql = """
            DELETE FROM loans WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        print(f"Loan {self.loan_type} | Amount: {self._loan_amount} successfuly deleted")

        # Delete from all and set id to None
        del type(self).all[self.id]
        self.id = None
