import sqlite3
import pandas as pd
from sys import argv
from os.path import (
    join,
    dirname,
    abspath
)


print('reading url_db.xlsx')
db = pd.read_excel(join(dirname(abspath(__file__)), 'url_db.xlsx'), 'Лист1')
print('reading names_db.xlsx')
name_db = pd.read_excel(join(dirname(abspath(__file__)), 'names_db.xlsx'), 'Лист1')
surname_db = pd.read_excel(join(dirname(abspath(__file__)), 'names_db.xlsx'), 'Лист2')


print('creating url.db')
conn = sqlite3.connect(join(dirname(abspath(__file__)), 'url.db'))
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS url(URL text, Title text, Section_1 text, Section_2 text)''')
ans = []
for j, val in enumerate(db['URL for compare']):
    ans.append((val.lower(), db['Title'][j], db['Section 1'][j], db['Section 2'][j]))
cur.executemany('''INSERT INTO url VALUES(?, ?, ?, ?)''', ans)
conn.commit()


print('creating names.db')
conn = sqlite3.connect(join(dirname(abspath(__file__)), 'names.db'))
cur = conn.cursor()
db = name_db
cur.execute('''CREATE TABLE IF NOT EXISTS name(GivenName text, Nameset text, Gender text)''')
ans = []
for j, val in enumerate(db['GivenName']):
    ans.append((val.lower(), db['NameSet'][j], db['Gender'][j]))
cur.executemany('''INSERT INTO name VALUES(?, ?, ?)''', ans)
conn.commit()


db = surname_db
cur.execute('''CREATE TABLE IF NOT EXISTS surname(Surname text, Nameset text, Gender text)''')
ans = []
for j, val in enumerate(db['Surname']):
    ans.append((val.lower(), db['NameSet'][j], db['Gender'][j]))
cur.executemany('''INSERT INTO surname VALUES(?, ?, ?)''', ans)
conn.commit()
print('done.')