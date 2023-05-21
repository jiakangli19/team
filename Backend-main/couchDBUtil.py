import couchdb

username = 'user'
password = 'pwd'



def getDB(tableName):
    url = f'http://{username}:{password}@172.26.134.204:5984/'
    couch = couchdb.Server(url)
    db = couch[tableName]
    return db


def getView(db, viewName):
    view = db.view(viewName, group_level=1)
    return view


if __name__ == '__main__':
    db = getDB()
    view = getView(db, 'city/city_num')
    for row in view:
        print(row)
