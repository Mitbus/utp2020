from pandas import read_excel
from pymorphy2 import MorphAnalyzer
from sqlite3 import connect
from os.path import (
    join,
    dirname,
    abspath
)


class Identifer:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = join(dirname(abspath(__file__)), "data/names.db")
        self.conn = connect(db_path)
        self.cur = self.conn.cursor()

    def detect(self, fio=None, name=None, surname=None, middle_name=None):
        tmp = []
        if fio is not None:
            for i in fio.lower().split(' '):
                if len(i) > 0:
                    tmp.append(i[0].upper() + i[1:])

        ans = {'first_name': None, 'middle_name': None, 'last_name': None, 'gender': None, 'nation': [None]}
        gender_by_name, gender_by_last_name, nation_by_name, nation_by_last_name = None, None, None, None
        name_ind, last_name_ind = -1, -1

        # find name
        if fio is None:
            tmp = []
            if name is not None:
                string = ''
                for n in name.split(' '):
                    if len(n) > 0:
                        string += n[0].upper() + n[1:].lower() + ' '
                tmp.append(string[:len(string) - 1])
        for ind, elem in enumerate(tmp):
            self.cur.execute('SELECT Nameset, Gender FROM name WHERE GivenName=?', [(elem.lower())])
            result = self.cur.fetchone()
            ans['first_name'] = elem
            name_ind = ind
            if result is not None:
                nation_by_name = result[0]
                gender_by_name = result[1]

        # find last name
        if fio is None:
            tmp = []
            if surname is not None:
                string = ''
                for sn in surname.split(' '):
                    if len(sn) > 0:
                        string += sn[0].upper() + sn[1:].lower() + ' '
                tmp.append(string[:len(string) - 1])
        for ind, elem in enumerate(tmp):
            if elem != ans['first_name']:
                self.cur.execute('SELECT Nameset, Gender FROM surname WHERE Surname=?', [(elem.lower())])
                result = self.cur.fetchone()
                ans['last_name'] = elem
                last_name_ind = ind
                if result is not None:
                    nation_by_last_name = result[0]
                    gender_by_last_name = result[1]

        # buliding middle name
        mid = ''
        if fio is None:
            tmp = []
            if middle_name is not None:
                mid += middle_name[0].upper() + middle_name[1:].lower()
        for i in range(len(tmp)):
            if i != name_ind and i != last_name_ind:
                mid += tmp[i] + ' '
        if mid != '':
            mid = mid[:len(mid) - 1]
            ans['middle_name'] = mid

        # detectig gender
        if gender_by_name is not None:
            ans['gender'] = gender_by_name
        elif gender_by_last_name is not None and gender_by_last_name != "None":
            ans['gender'] = gender_by_last_name
        else:
            morph = MorphAnalyzer()
            if len(mid) > 0:
                n_mid = morph.parse(mid)[0].normal_form
                if n_mid[len(n_mid) - 1] == 'ч':
                    ans['gender'] = 'male'
                elif n_mid[len(n_mid) - 1] == 'а':
                    ans['gender'] = 'female'
            elif gender_by_last_name == "None":
                gender = morph.parse((tmp[last_name_ind]))[0].tag.gender
                if gender == "masc":
                    ans['gender'] = 'male'
                elif gender == "femn":
                    ans['gender'] = 'female'

        # detection nation
        if nation_by_name == nation_by_last_name:
            ans['nation'] = [nation_by_name]
        elif nation_by_name is None:
            ans['nation'] = [nation_by_last_name]
        elif nation_by_last_name is None:
            ans['nation'] = [nation_by_name]
        else:
            ans['nation'] = [nation_by_name, nation_by_last_name]

        return ans

