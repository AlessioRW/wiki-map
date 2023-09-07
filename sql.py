import sqlite3

conn = sqlite3.connect('./data.sqlite')
db = conn.cursor()

def create_table():
    try:
        db.execute('DROP TABLE pages;')
    except:
        pass
    try:
        db.execute('DROP TABLE connections;')
    except:
        pass

    pages_query = 'CREATE TABLE pages (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, page STRING NOT NULL, connections STRING);'
    db.execute(pages_query)
    conn.commit()
#create_table()

def toLower():
    db.execute('UPDATE pages SET page = LOWER(page)')
    conn.commit()
#toLower()
