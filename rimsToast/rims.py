import traceback

import requests
import yaml
import time

from rimsToast.fileMap import *
from rimsToast.toast import pc_toast

_url = 'https://rims.croot.com'

# 缓存文件
_file = "properties.txt"

def get_conf():
    with open("config.yaml", "r", encoding='utf8') as config:
        data = yaml.safe_load(config)
        return data

def login(conf):
    payload = {
        'optid': conf['rims']['login']['optid'],
        'optpwd': conf['rims']['login']['optpwd'],
        'encrypted': conf['rims']['login']['encrypted'],
    }
    try:
        resp = requests.post(url=_url + '/api/rms/operator/login', data=payload)
        jsonStr = resp.json()
        resp.close()
        print('登录返回：'+str(jsonStr))
        if jsonStr['code'] == 0:
            file_put(_file, _url, jsonStr['data']['uuid'])
            return jsonStr['data']['uuid']
    except Exception:
        traceback.print_exc()


def get_uuid(conf):
    uuid = file_get(_file, _url)
    if uuid is None:
        uuid = login(conf)
    return uuid


def get_header(conf):
    header = {
        'uuid': get_uuid(conf)
    }
    return header

## 获取我的待办
def _get_work_result(type, header):
    try:
        resp = requests.get(url=_url + '/api/rms/workBench/total?type=' + type, headers=header)
        result_json = resp.json()
        # print(str(result_json))
        resp.close()
        return result_json['data']
    except Exception:
        traceback.print_exc()
        print('_get_work_result fail')
    return []

def _get_work_data(type, header):
    work_data = _get_work_result(type, header)
    data = {}
    for x in work_data:
        data[x['type']] = x['total']
    return data

def rims_toast(conf, text):
    pc_toast(conf['toast']['title'], text, conf['toast']['icon_path'])

# 自定义get方法
def _get(obj, name):
    if name not in obj:
        return 0
    else:
        return obj[name]

## 检查登录
def _check_login(conf, header):
    try:
        resp = requests.get(url=_url + '/api/rms/workBench/scheduleMyVersion', headers=header)
        result_json = resp.json()
        resp.close()
        if result_json['code'] == 2007:
            login(conf)
    except Exception:
        traceback.print_exc()
        print('_check_login fail')

if __name__ == '__main__':
    conf = get_conf()
    header = get_header(conf)
    _check_login(conf, header)

    work_data = _get_work_data(conf['rims']['todo'], header)

    while 1 == 1:
        time.sleep(conf['toast']['interval'])
        new_work_data = _get_work_data(conf['rims']['done'], header)
        message = []
        for x in conf['rims']['check']:
            count = _get(new_work_data, x['type'])
            if _get(work_data, x['type']) != count:
                message.append(x['name'] + '有变化啦，总数：' + str(count) + '\n')
        rims_toast(conf, ''.join(message))