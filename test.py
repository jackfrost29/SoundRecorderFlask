import sqlite3
import codecs

db_file = 'database.db'


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_file)
        db.row_factory = make_dicts
    return db


conn = sqlite3.connect(db_file)
conn.row_factory = make_dicts

cur = conn.cursor()

d = sorted(cur.execute('select * from sentence_table where status = ?;', ('recorded', )).fetchall(), key=lambda x:x['id'])



cur.close()
conn.close()

with codecs.open('wiki-from-sqlite.txt', mode='w+', encoding='utf-8') as f:
    for dic in d:
        f.write(f'{dic["id"]}|{dic["sentence"]}\n')

