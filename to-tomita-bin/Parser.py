from subprocess import Popen
from json import loads
from recobj.data.geo_deskr import sokr
from os import system
from os.path import (
    join,
    dirname,
    abspath
)


def preprocess(string):
    for s in sokr:
        new_s = s.replace(".", "@")
        string = string.replace(s, new_s)
    return string


def interpretate(string):
    with open(join(dirname(abspath(__file__)), "_input"),
    'w', encoding='utf8') as f:
        f.write(string)
    system("cd " + str(dirname(abspath(__file__))) + "; ./tomita-parser config.proto")
    with open(join(dirname(abspath(__file__)), "_output"),
    'r', encoding='utf8') as f:
        string = f.read()
    return string


def postprocess(string):
    string = string.replace(" @", ".")
    obj = loads(string)
    ret_obj = {}

    def construct_fact(fact):
        fact_obj = {
            'pos': fact['Attr']['TextPos'],
            'len': fact['Attr']['TextLen']
        }
        for i in fact['Field']:
            fact_obj[i['Name']] = i['Value']
        return fact_obj

    for fact in obj[0]['FactGroup']:
        for fact_type in ('fio_fact', 'geo_fact', 'ts_fact', 'ip_fact', 'bank_fact'):
            if fact['Type'] == fact_type:
                ret_obj[fact_type] = []
                for f in fact['Fact']:
                    ret_obj[fact_type].append(construct_fact(f))

        # process url_fact differently
        if fact['Type'] == 'url_fact':
            ret_obj['url_fact'] = []
            for url_f in fact['Fact']:
                url_f['Field'][0]['Value'] = url_f['Field'][0]['Value'].replace(' ', '').lower()
                ret_obj['url_fact'].append(construct_fact(url_f))
    return ret_obj


def parse(string):
    return postprocess(interpretate(preprocess(string)))
