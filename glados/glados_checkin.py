# encoding=utf8

import io
import os
import sys
import time

import urllib3

from push_message import *

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def __get_header(cookie_header):
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

split_str = '&@@&'

# def glados_checkIn(glados_cookie):
#     checkin_message = []
#     # 判断是否设置
#     if glados_cookie is None or len(glados_cookie) <= 0:
#         print("The glados_cookie is none")
#         return checkin_message
#
#     glados_cookie = glados_cookie.split(split_str)
#     # 遍历cookie执行签到，并返回签到状态码和签到信息
#     for idx, cookie in enumerate(glados_cookie):
#         time.sleep(10)
#         print(f"[glados_Account_{idx + 1}]:")
#         header = __get_header(cookie)
#         result = checkIn(header)
#         # 存在账户签到信息，说明成功执行了签到
#         checkin_message.append(f">### glados_Account_{idx + 1} checkin message\n" + str(result) + "\n - - - \n")
#     return checkin_message
#
# # 单条签到
# def checkIn(header):
#     checkin_message = []
#     # 1、签到
#     result_json = _check_in(header)
#
#     code = result_json["code"]
#     message = result_json["message"]
#     usr_status = getStatus(header)
#
#     checkin_message.append("**【签到状态码】**  " + str(code) + " <br>")
#     checkin_message.append("**【签到信息】**  " + str(message) + " <br>")
#     checkin_message.append("**【email】**  " + str(_get(usr_status, 'email')) + " <br>")
#     checkin_message.append("**【剩余天数】**  " + str(_get(usr_status, 'days')) + " <br>")
#
#     return ''.join(checkin_message)

# 签到
def _check_in(header):
    result_json = {}
    data = {
        "token": "glados.network"
    }
    try:
        # 1、签到
        resp = requests.post(url='https://glados.rocks/api/user/checkin', headers=header, json=data)
        result_json = resp.json()
        print('[_check_in response]', str(result_json))
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

if __name__ == '__main__':
    # glados平台cookie
    juejin_cookie = os.environ['GLADOS_COOKIE']
    # pushplus平台token
    pushplus_token = os.environ['PUSHPLUS_TOKEN']

    header = __get_header(juejin_cookie)

    checkin_message = []
    # 1、签到
    result_json = _check_in(header)

    code = result_json["code"]
    message = result_json["message"]
    usr_status = getStatus(header)

    checkin_message.append("**【签到状态码】**  " + str(code) + " <br>")
    checkin_message.append("**【签到信息】**  " + str(message) + " <br>")
    checkin_message.append("**【email】**  " + str(_get(usr_status, 'email')) + " <br>")
    checkin_message.append("**【剩余天数】**  " + str(_get(usr_status, 'days')) + " <br>")

    send_message = ''.join(checkin_message)

    # 第一次推送
    msg = pushplus_message(pushplus_token, message, send_message, None)
    if msg is not None:
        # 推送失败再次推送
        time.sleep(10)
        pushplus_message(pushplus_token, '再次推送,首次推送失败:' + msg, send_message, None)