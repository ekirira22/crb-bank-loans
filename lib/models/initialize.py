import sqlite3

CONN = sqlite3.connect('bankdata.db')
CURSOR = CONN.cursor()
