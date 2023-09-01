import sqlite3


target = 'Graph_theory'
conn = sqlite3.connect('./data.sqlite')
db = conn.cursor()
max_depth = 5
def search(page, depth):
    
    target_query = "SELECT COUNT(*) FROM connections WHERE page = '{}' AND sub_page = '{}'".format(page,target)
    exists = db.execute(target_query).fetchone()[0]
    if exists > 0:
        print('connection found')
        print(page)
        return
    else:
        if  depth == max_depth:
            return
        sub_pages_query = "SELECT sub_page FROM connections WHERE page = '{}'".format(page)
        sub_pages = db.execute(sub_pages_query).fetchall()
        for sub_page in sub_pages:
            sub_page_title = sub_page[0]
            search(sub_page_title, depth+1)

search('Grochocice', 0 )