from pandas import read_excel
from sqlite3 import connect
from os.path import (
    join,
    dirname,
    abspath
)


class UrlHandler:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = join(dirname(abspath(__file__)), "data/url.db")
        self.conn = connect(db_path)
        self.cur = self.conn.cursor()

    def find(self, url):
        url = url.lower()
        if url[:7] == "http://":
            url = url[7:]
        elif url[:8] == "https://":
            url = url[8:]
        if url[:4] == "www.":
            url = url[4:]
        len_url = len(url)
        if url[len_url - 1] == "/":
            url = url[:len_url - 1]
        url += "/"
        for i in range(url.count("/")):
            url = url[:url.rfind("/")]
            self.cur.execute('SELECT Title, Section_1, Section_2 FROM url WHERE URL=?', [(url)])
            result = self.cur.fetchone()
            if result is not None:
                return {'Title': result[0], 'Section': (result[1], result[2])}
        return None
