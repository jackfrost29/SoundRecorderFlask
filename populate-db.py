exit()

text_file = 'wiki_dataset_final.txt'
db_file = 'database.db'



import sqlite3
from numpy import int32
from pandas import read_csv, DataFrame
int32

id = 'id'
sentence = 'sentence'
status = 'status'
table_name = 'sentence_table'

conn = sqlite3.connect(db_file)
c = conn.cursor()

c.execute("""DROP TABLE IF EXISTS sentence_table""")
c.execute("""
CREATE TABLE sentence_table(
id INTEGER PRIMARY_KEY,
sentence TEXT,
status TEXT)""")

df = read_csv(text_file, delimiter='|', encoding='utf-8', header=None, dtype={0: int32})
df.columns = [id, sentence, status]

df.to_sql(table_name, conn, if_exists='append', index=False, method='multi')

conn.commit()
conn.close()
