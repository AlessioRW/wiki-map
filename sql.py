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

    pages_query = 'CREATE TABLE pages (page STRING);'
    connections_query = 'CREATE TABLE connections (page string, sub_page string);'
    #db.execute(pages_query)
    db.execute(connections_query)
    conn.commit()

create_table()