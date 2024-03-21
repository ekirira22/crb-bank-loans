from __init__ import CURSOR, CONN
import ipdb
class Bank:

    all = {}

    def __init__(self, name, branch, id=None) -> None:
        self.name = name
        self.branch = branch
        self.id = id
        print(f"Added {self.name} bank | {self.branch} branch successfully")


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
        if isinstance(name, str) and len(name) > 1:
            self._name = name
            return
        raise TypeError("Bank name has to be a valid name")
    
    @property
    def branch(self):
        return self._branch
    
    @branch.setter
    def branch(self, branch):
        if isinstance(branch, str) and len(branch) > 1:
            self._branch = branch
            return
        raise TypeError("Branch name has to be a valid name")
    
    """
        ORM CLASS METHODS
    """
    @classmethod
    def create_table(cls) -> None:
        # Create a new table to persist the attributes of Bank instances
        sql = """
            CREATE TABLE IF NOT EXISTS banks (
                id INT PRIMARY KEY,
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
        # Delete the table row corresponding to the current Bank instance
        sql = """
            DELETE FROM banks WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

    
Bank.drop_table()
Bank.create_table()

equity = Bank("Equity Bank", "Nyeri")
coop = Bank.create("Coop", "Nairobi")
ipdb.set_trace()



