# encoding=utf8

import io
import os
import sys
import time

import urllib3

from push_message import *

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def _get_header(cookie_header):
    header = {
        'Connection': 'close',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'cookie': cookie_header,
        'Content-Type': 'application/json;charset=UTF-8',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                      " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "Windows",
        'sec-fetch-dest': "empty",
        'sec-fetch-mode': "cors",
        'sec-fetch-site': "same-origin"
    }
    return header


# 解决出现警告 Adding certificate verification is strongly advised.
urllib3.disable_warnings()

# 分隔符
split_str = '&@@&'

def batch_checkIn(glados_cookie):
    result_list = []
    # 判断是否设置
    if glados_cookie is None or len(glados_cookie) <= 0:
        print("The glados_cookie is none")
        return result_list

    glados_cookie = glados_cookie.split(split_str)
    # 遍历cookie执行签到，并返回签到状态码和签到信息
    for idx, cookie in enumerate(glados_cookie):
        time.sleep(10)
        print(f"[glados_Account_{idx + 1}]:")
        header = _get_header(cookie)
        result = checkIn(header)
        # 存在账户签到信息，说明成功执行了签到
        result_list.append(result)
    return result_list

# 单条签到
def checkIn(header):
    # 1、签到
    result_json = _check_in(header)

    code = result_json["code"]
    message = result_json["message"]
    usr_status = getStatus(header)

    data = {
        'code': str(code),
        'message': str(message),
        'email': str(_get(usr_status, 'email')),
        'leftDays': str(_get(usr_status, 'leftDays'))
    }
    return data

# 签到
def _check_in(header):
    result_json = {}
    data = {
        "token": "glados.one"
    }
    try:
        # 1、签到
        resp = requests.post(url='https://glados.rocks/api/user/checkin', headers=header, json=data)
        result_json = resp.json()
        print('[_check_in response]', result_json['code'] ,result_json['message'])
        resp.close()
    except Exception:
        traceback.print_exc()
        print('_check_in fail')
        result_json['code'] = -1
        result_json['message'] = '签到出现异常(灬ꈍ ꈍ灬)'
    return result_json

# 自定义get方法
def _get(obj, name):
    if name not in obj:
        return None
    else:
        return obj[name]

# 用户状态
def getStatus(header):
    status_data = {}
    try:
        resp = requests.get(url='https://glados.rocks/api/user/status', headers=header)
        result_json = resp.json()
        print('[getStatus response]', str(result_json))
        resp.close()
        if result_json["code"] != 0:
            print("getStatus fail : ", result_json["message"])
        else:
            status_data = result_json["data"]
    except Exception:
        traceback.print_exc()
        print('getStatus fail')
    return status_data

# 封装推送信息
def _get_message(result_list):
    title = []
    message = []
    # enumerate函数中通过start参数指定从1开始数数，遍历还是从下标0开始
    for idx, data in enumerate(result_list, start=1):
        title.append(f"{idx}")
        if data['code'] == '0':
            title.append(f"-{data['code']};")
        else:
            title.append("*R;")
        message.append(f">### glados_Account_{idx} checkin message\n")
        message.append("**【签到状态码】**  " + data['code'] + " <br>")
        message.append("**【签到信息】**  " + data['message'] + " <br>")
        message.append("**【email】**  " + data['email'] + " <br>")
        message.append("**【剩余天数】**  " + data['leftDays'] + " <br>")
        message.append("\n - - - \n")
    return ''.join(title), ''.join(message)

if __name__ == '__main__':
    # glados平台cookie
    glados_cookie = os.environ['GLADOS_COOKIE']
    # pushplus平台token
    pushplus_token = os.environ['PUSHPLUS_TOKEN']

    result_list = batch_checkIn(glados_cookie)
    title, send_message = _get_message(result_list)

    # print(send_message)
    # 第一次推送
    msg = pushplus_message(pushplus_token, title, send_message, None)
    if msg is not None:
        # 推送失败再次推送
        time.sleep(10)
        pushplus_message(pushplus_token, '再次推送,首次推送失败:' + msg, send_message, None)
