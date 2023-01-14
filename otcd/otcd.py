import os
import traceback

import requests
import csv
from util import *

urls = {
    "1": 'http://172.22.19.20:8095',
    "2": 'http://192.168.2.46:8095'
}
_url = urls["1"]

# 缓存文件
_file = "properties.txt"


payload={
    'optid': '99990',
    'optpwd': 'WDY4aJqKQ0Ee64zEFsJGUA==',
    'encrypted': 'true'
}

def login():
    try:
        resp = requests.post(url=_url + '/operator/login', data=payload)
        jsonStr = resp.json()
        resp.close()
        print(jsonStr)
        if jsonStr['code'] == 0:
            file_put(_file, _url, jsonStr['data']['uuid'])
            return jsonStr['data']['uuid']
    except Exception:
        traceback.print_exc()

def get_uuid():
    uuid = file_get(_file, _url)
    if uuid is None:
        uuid = login()
    return uuid

def get_header():
    header = {
        'uuid': get_uuid()
    }
    return header

def calcScale(_header):
    ids = [
        # '1000000069',
        '1000000070',
        # '1000000071',
        # '1000000072',
        # '1000000073',
        # '1000000074',
        # '1000000077',
        # '1000000079',
        # '1000000109',
        # '1000000110',
        # '1000000111',
        # '1000000112',
        # '1000000113',
        # '1000000114',
        # '1000000115',
        # '1000000116',
        # '1000000117',
        # '1000000118',
        # '1000000119',
        # '1000000120',
        # '1000000121',
        # '1000000122',
        # '1000000123',
        # '1000000124',
        # '1000000125',
        # '1000000126',
        # '1000000127',
        # '1000000128',
        # '1000000129',
    ]
    data = [

    ]
    for id in ids:
        resp = requests.get(url=_url + '/option/contract/test/'+id, headers=_header)
        jsonStr = resp.json()
        resp.close()
        row = []
        # print(jsonStr)
        if jsonStr['code'] == 0:
            print(id + ' ' + str(jsonStr['data'][0]) + ' ' + str(jsonStr['data'][1]))
            row.append(id)
            row.append(str(jsonStr['data'][0]))
            row.append(str(jsonStr['data'][1]))
            data.append(row)
    return data

def write_csv(data):
    with open('text.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerows(data)

if __name__ == '__main__':
    # login()
    header = get_header()
    data = calcScale(header)
    # write_csv(data)