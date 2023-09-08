import sqlite3




def search(page_id, depth, cur_path, target, max_depth):
    global paths
    if type(page_id) == str:
        
        id_res = db.execute('SELECT id FROM pages WHERE page LIKE "{}"'.format(page_id)).fetchone()
        if id_res:
            page_id = id_res[0]
            
        else:
            return 
    page_info_res = db.execute('SELECT * FROM pages WHERE id == {}'.format(page_id))
    if page_info_res:
        page_info = page_info_res.fetchone()
        page_name = str(page_info[1])

        if page_name in cur_path:
            return
        cur_path.append(page_name)
        
        if page_name.lower() == target.lower():
            paths += ','.join(cur_path) + '&'
            cur_path.pop()
            return


        if len(cur_path) > max_depth:
            cur_path.pop()
            return
        
        connections = page_info[2]
        if type(connections) == int:
            connections = str(connections)
        if connections != None and len(connections) > 0:
            
            for next_id in connections.split(','):
                search(int(next_id), depth+1, cur_path, target, max_depth)

    cur_path.pop()
    return

def get_connections(start, target, max_depth):
    global conn
    global db
    global paths
    
    conn = sqlite3.connect('./data.sqlite')
    db = conn.cursor()
    paths = ''

    search(start, 0, [], target, max_depth)
    
    return paths.split('&')

x = get_connections('united_kingdom', 'london', 10)
print(x)