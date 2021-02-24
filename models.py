import os
import json
from sqlobject import SQLObject, sqlhub, connectionForURI, StringCol, BigIntCol
import sqlite3

db_filename = os.path.abspath('data.db')
connection_string = 'sqlite:' + db_filename
connection = connectionForURI(connection_string)
sqlhub.processConnection = connection


class Song(SQLObject):
    name = StringCol()
    artist = StringCol()
    art = StringCol()
    url = StringCol()
    added = BigIntCol()
    tags = StringCol()
    lyrics = StringCol()

    def to_dict(self):
        if self.tags == '':
            tags = []
        else:
            tags = json.loads(self.tags)

        return {
            'id': self.id,
            'name': self.name,
            'artist': self.artist,
            'art': self.art,
            'added': self.added,
            'url': self.url,
            'lyrics': self.lyrics,
            'tags': tags
        }


Song.createTable(ifNotExists=True)

def migrate():
    sqlite_conn = sqlite3.connect('data.db')

    try:
        sqlite_conn.execute("ALTER TABLE song ADD COLUMN lyrics TEXT default ''")
    except Exception as e:
        print(e)

    sqlite_conn.close()

migrate()