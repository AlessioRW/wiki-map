import sqlite3

conn = sqlite3.connect('./data.sqlite')
db = conn.cursor()

def create_table():
    ch = input('are you sure you want to reset the database?(yes/no): ')
    if 'yes' not in ch.lower():
        return
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

def to_lower():
    db.execute('UPDATE pages SET page = LOWER(page)')
    conn.commit()
#to_lower()

def count_connections():
    total = 0
    connection_list = db.execute('SELECT connections FROM pages').fetchall()
    for connections in connection_list:
        try:
            total += len(str(connections[0]).split(','))
        except:
            print(connections[0])
            return
    print('Total Connections: ',total)

count_connections()