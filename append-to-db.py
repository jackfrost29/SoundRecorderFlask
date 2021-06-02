exit()


text_file = 'new_sentence.txt'
db_file = 'database.db'


id = 'id'
sentence = 'sentence'
status = 'status'
table_name = 'sentence_table'


import sqlite3
from numpy import int32
from pandas import read_csv, DataFrame
int32


conn = sqlite3.connect(db_file)
c = conn.cursor()


df = read_csv(text_file, delimiter='|', encoding='utf-8', header=None, dtype={0: int32})
df.columns = [id, sentence, status]

df.to_sql(table_name, conn, if_exists='append', index=False, method='multi')

conn.commit()
conn.close()
