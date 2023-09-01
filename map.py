from bs4 import BeautifulSoup
import requests, sqlite3

blacklist = [
    'Category:',
    'Wikipedia:',
    'File:',
    'Special:',
    'Template:',
    'Talk:',
    'Portal:',
    'Help:',
    'User:',
    'Template_talk:',
    'Main_Page',
]


conn = sqlite3.connect('./data.sqlite')
db = conn.cursor()
total_added = 0
max_depth = 5
def map_pages(url,depth):
    global total_added
    
    # if total_added % 100 == 0:
    #     print('connections made: {}'.format(total_added))
    req = requests.get(url)
    parser = BeautifulSoup(req.text, 'html.parser')
    cur_page = parser.find_all('link', {'rel':'canonical'})[0]['href'].split('/wiki/')[1]
        
    pages = []
    for link in parser.find_all('a'):
        if (link.get('href')):
            skip = False
            for term in blacklist:
                if term in link.get('href'):
                    skip = True
            if skip:
                continue
            if link.get('href')[0:6] == '/wiki/':
                if link.get('href') not in pages:
                    pages.append(link.get('href')[6:])

    for page in pages:
        if page == cur_page:
            continue
        exists_query = "SELECT COUNT(*) FROM connections WHERE page == '{}';".format(page)
        exists = db.execute(exists_query).fetchone()[0]
        if exists > 0:
            return

        connection_query = "INSERT INTO connections (page, sub_page) VALUES ('{}', '{}');".format(cur_page, page)
        db.execute(connection_query)
        total_added += 1
        conn.commit()

        if depth > max_depth:
            return
        else:
            new_url = 'https://en.wikipedia.org/wiki/{}'.format(page)
            map_pages(new_url,depth+1)

map_pages('https://en.wikipedia.org/wiki/Special:Random',0)