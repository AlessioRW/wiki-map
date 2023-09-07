from bs4 import BeautifulSoup
import requests, sqlite3, os


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
    'Geographic_coordinate_system',
]


conn = sqlite3.connect('./data.sqlite')
db = conn.cursor()
total_added = 0
fail_counter = 0
max_depth = 6
def map_pages(url,depth):
    global total_added
    global fail_counter

    try:
        req = requests.get(url)
    except:
        print('Network Error: Could not retrieve',url)
        return
    
    parser = BeautifulSoup(req.text, 'html.parser')

    external_link_tag = parser.find('span', {'id':'External_links'})
    if external_link_tag:
        for tag in external_link_tag.find_all_next():
            tag.clear()

    cur_page = parser.find_all('link', {'rel':'canonical'})[0]['href'].split('/wiki/')[1]
    cur_page = cur_page.replace("'",'\'')

    try:
        cur_page_data = db.execute('SELECT * FROM pages WHERE page == "{}";'.format(cur_page)).fetchone()
    except Exception as e:
        print('Error:',e)
        print(cur_page)
        return
    if cur_page_data:
        cur_page_id = cur_page_data[0]
        
    else:
        db.execute('INSERT INTO pages (page) VALUES ("{}")'.format(cur_page))
        cur_page_id = db.lastrowid
        cur_page_data = db.execute('SELECT * FROM pages WHERE id == "{}";'.format(cur_page_id)).fetchone()
    conn.commit()

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

    if cur_page_data[2]:
        cur_page_connections = str(cur_page_data[2]).split(',')
    else:
        cur_page_connections = []
    for page in pages:
        page_id = -1
        if page == cur_page:
            continue
        
        try:
            page_id_res = db.execute('SELECT (id) FROM pages WHERE page == "{}"'.format(page)).fetchone()
        except Exception as e:
            print('Error:',e)
            print(cur_page)
            continue
        if page_id_res:
            page_id = page_id_res[0]
        else:
            db.execute('INSERT INTO pages (page) VALUES ("{}")'.format(page))
            page_id = db.lastrowid
        
        if str(page_id) in cur_page_connections:
            return
        else:
            cur_page_connections.append(str(page_id))
            new_connections = ','.join(cur_page_connections)
            db.execute('UPDATE pages SET connections = "{}" WHERE id = {}'.format(new_connections, cur_page_id))
            conn.commit()

            # total_added += 1
            # if total_added % 50 == 0:
            #     os.system('cls')
            #     print('connections made: {}'.format(total_added))

            if depth > max_depth:
                return
            else:
                new_url = 'https://en.wikipedia.org/wiki/{}'.format(page)
            map_pages(new_url,depth+1)

        

        

print('Mapping Started')
map_pages('https://en.wikipedia.org/wiki/Special:Random',0)