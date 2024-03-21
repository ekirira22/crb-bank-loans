import sqlite3

CONN = sqlite3.connect('bank.db')
CURSOR = CONN.cursor()
