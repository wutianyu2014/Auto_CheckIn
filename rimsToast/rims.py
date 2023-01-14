import time

from util import *
from util.toast import pc_toast

urls = {
    "1": 'https://rims.croot.com'
}
_url = urls["1"]

# 缓存文件
_file = "properties.txt"

payload = {
    'optid': 'wutianyu',
    'optpwd': 'Wty210419',
    'encrypted': 'false'
}


def login():
    try:
        resp = requests.post(url=_url + '/api/rms/operator/login', data=payload)
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
        print('_get_work fail')
    return []


def _get_work_data(type, header):
    work_data = _get_work_result(type, header)
    data = {}
    for x in work_data:
        data[x['type']] = x['total']
    return data


def rims_toast(text):
    pc_toast("您有新的rims待办", text, 'E:\RootNetLogo.ico')

# 自定义get方法
def _get(obj, name):
    if name not in obj:
        return 0
    else:
        return obj[name]

# 检查项
_check_type = [
    {"type": "defect", "name": 'bug'},
    {"type": "issue", "name": '缺陷'},
    {"type": "tracer", "name": '研发任务'}
]

if __name__ == '__main__':
    header = get_header()
    work_data = _get_work_data('2', header)

    while 1 == 1:
        time.sleep(2)
        new_work_data = _get_work_data('1', header)
        message = []
        for x in _check_type:
            count = _get(new_work_data, x['type'])
            if _get(work_data, x['type']) != count:
                message.append(x['name'] + '有变化啦，总数：' + str(count) + '\n')
        rims_toast(''.join(message))