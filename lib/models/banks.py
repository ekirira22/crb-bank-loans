#! /usr/bin/env python3
from models.initialize import CURSOR, CONN
class Bank:

    all = {}

    def __init__(self, name, branch, id=None) -> None:
        self.id = id
        self.name = name
        self.branch = branch
    # Returns details of instance
    def __repr__(self) -> str:
        return f"<Bank {self.id}: {self.name} | {self.branch}>"
    
    """
        PROPERTY METHODS
    """
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name) > 0:
            self._name = name
            return
        raise TypeError("Bank name has to be a string and length greater than 0")
    
    @property
    def branch(self):
        return self._branch
    
    @branch.setter
    def branch(self, branch):
        if isinstance(branch, str) and len(branch) > 0:
            self._branch = branch
            return
        raise TypeError("Branch name has to be a string and length greater than 0")
    
    """
        ORM CLASS METHODS
    """
    @classmethod
    def create_table(cls) -> None:
        # Create a new table to persist the attributes of Bank instances
        sql = """
            CREATE TABLE IF NOT EXISTS banks (
                id INTEGER PRIMARY KEY,
                name TEXT,
                branch TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls) -> None:
        # Drop the table to persist the attributes of Bank instances
        sql = """
            DROP TABLE IF EXISTS banks;
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def create(cls, name, branch):
        new_bank = cls(name, branch)
        new_bank.save()
        return new_bank
    
    @classmethod
    def instance_from_db(cls, result):
        # first check if it exists in all dict
        if bank := cls.all.get(result[0]):
            # Reset values incase of any alteration
            bank.name = result[1]
            bank.branch = result[2]
        else:
            # not in dictionary but in db
            bank = cls(result[1], result[2])
            bank.id = result[0]
            cls.all[bank.id] = bank
        return bank
    
    @classmethod
    def get_all(cls):
        # Return a list containing a Bank object per row in the table
        sql = """
            SELECT * FROM banks
        """
        results = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(result) for result in results]
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM banks WHERE id = ?
        """
        result = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(result) if result else None
    
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * FROM banks WHERE name = ?
        """
        result = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(result) if result else None

    """
        ORM CRUD INSTANCE METHODS
    """

    def save(self) -> None:
        # Insert a new row with the name and branch values of the current Bank instance. 
        # Update object id attribute using the primary key value of new row.

        sql = """
            INSERT INTO banks (name, branch) VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.branch))
        CONN.commit()

        # Now store the ID
        self.id = CURSOR.lastrowid

        # Save this bank instance in a dictionary with id as the key
        type(self).all[self.id] = self

    def update(self):
        # Update the table row corresponding to the current Bank instance.
        sql = """
            UPDATE banks SET name = ?, branch = ? WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.branch, self.id))
        CONN.commit()

    def delete(self):
        from models.loans import Loan
        # Deletes by Association - delete all banks with loans associated to this bank instance
        # before deleting the bank itself

        loans_delete_ids = [loan.id for loan in Loan.get_all() if loan.bank_id is self.id]
        [Loan.delete_by_id(id) for id in loans_delete_ids]
       
        # Delete the table row corresponding to the current Bank instance
        sql = """
            DELETE FROM banks WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete from all and set id to None
        del type(self).all[self.id]
        self.id = None


        


