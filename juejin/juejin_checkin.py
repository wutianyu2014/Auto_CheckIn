# encoding=utf8

import io
import sys
import time
import traceback

import requests
import urllib3

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# url
_url = 'https://api.juejin.cn/growth_api/v1'

def _get_header(cookie_header):
    header = {
        'Connection': 'close',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'cookie': cookie_header,
        'Content-Type': 'application/json;charset=UTF-8',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                      " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "Referer": "https://juejin.cn/",
        "Accept-Encoding": "gzip, deflate",
    }
    return header

# 解决出现警告 Adding certificate verification is strongly advised.
urllib3.disable_warnings()

split_str = '&@@&'

def batch_checkIn(juejin_cookie):
    result_list = []
    # 判断是否设置
    if juejin_cookie is None or len(juejin_cookie) <= 0:
        print("The juejin_cookie is none")
        return result_list

    juejin_cookie = juejin_cookie.split(split_str)
    # 遍历cookie执行签到，并返回签到状态码和签到信息
    for idx, cookie in enumerate(juejin_cookie, start=1):
        time.sleep(10)
        print(f"[juejin_Account_{idx}]:")
        header = _get_header(cookie)
        data = check_in_new(idx, header)
        # 为none代表已签到
        if data is not None:
            result_list.append(data)
    return result_list

# 拼接推送内容，如果全部签到成功，title为空字符串
def get_send_content(result_list):
    title = []
    message = []
    # enumerate函数中通过start参数指定从1开始数数，遍历还是从下标0开始
    for idx, data in enumerate(result_list, start=1):
        message.append(f">### juejin_Account_{data['inx']} checkin message\n")
        if data['code'] == '0':
            message.append("![](" + data['icon'] + ") <br>")
        else:
            title.append(f"{data['inx']}{data['code']}-")
        message.append("**【签到状态码】**  " + data['code'] + " <br>")
        message.append("**【签到信息】**  " + data['message'] + " <br>")
        if data['code'] == '0':
            message.append("**【获取矿石数】**  " + data['incr_point'] + " <br>")
            message.append("**【连续签到天数】**  " + data['cont_count'] + " <br>")
            message.append("**【总签到天数】**  " + data['sum_count'] + " <br>")
            message.append("**【抽奖增加幸运值】**  " + data['draw_lucky_value'] + " <br>")
            message.append("**【总幸运值】**  " + data['total_lucky_value'] + " <br>")
            message.append("**【抽奖结果】**  " + data['lottery_name'] + " <br>")
            message.append("**【矿石总量】**  " + data['sum_point'] + " <br>")
            message.append("![](" + data['lottery_image'] + ") <br>")
        message.append("\n - - - \n")
    return ''.join(title), ''.join(message)

# 单条签到
def check_in_new(idx, header):
    # 1、先判断是否签到
    resp = requests.get(url=_url + '/get_today_status', headers=header)
    status_json = resp.json()
    print('[get_today_status response]', str(status_json))
    resp.close()
    # 1.1 获取状态失败
    if status_json["err_no"] != 0 or status_json["err_msg"] != 'success':
        data = {
            'inx': idx,
            'code': 'N',
            'message': str(status_json["data"])
        }
        return data

    # 1.2 已签到过
    if status_json["data"]:
        print("Signed in")
        return None
    # 1.3 未签到逻辑

    # 2、开始签到
    requests.get("https://juejin.cn/", headers=header)
    time.sleep(10)
    requests.get("https://juejin.cn/user/center/signin?from=main_page", headers=header)
    time.sleep(10)
    result_json = _check_in(header)
    requests.get("https://juejin.cn/user/center/lottery?from=lucky_lottery_menu_bar", headers=header)
    time.sleep(10)
    requests.get("https://juejin.cn/notification", headers=header)
    time.sleep(10)

    err_no = result_json["err_no"]
    err_msg = result_json["err_msg"]

    if err_no != 0:
        # 2.1、签到失败
        print("check in fail : ", err_msg)
        data = {
            'inx': str(idx),
            'code': 'N',
            'message': str(err_msg)
        }
        return data
    # 2.2、签到成功
    incr_point = result_json["data"]["incr_point"]
    # 3、抽奖
    draw_data = draw(header)
    # 4 获取总矿石
    sum_point = get_cur_point(header)
    # 5 获取连签天数
    cont_count, sum_count = get_counts(header)
    # 6 获取用户头像
    icon = get_user_icon(header)

    data = {
        'inx': str(idx),
        'code': str(err_no),
        'message': str(err_msg),
        'icon': str(icon),
        'incr_point': str(incr_point),
        'cont_count': str(cont_count),
        'sum_count': str(sum_count),
        'draw_lucky_value': str(_get(draw_data, 'draw_lucky_value')),
        'total_lucky_value': str(_get(draw_data, 'total_lucky_value')),
        'lottery_name': str(_get(draw_data, 'lottery_name')),
        'sum_point': str(sum_point),
        'lottery_image': str(_get(draw_data, 'lottery_image'))
    }
    return data

def _get_msg(data):
    message = []
    message.append(f">### juejin_Account_{data['inx']} checkin message\n")
    if data['code'] == '0':
        message.append("![](" + data['icon'] + ") <br>")
    message.append("**【签到状态码】**  " + data['code'] + " <br>")
    message.append("**【签到信息】**  " + data['message'] + " <br>")
    if data['code'] == '0':
        message.append("**【获取矿石数】**  " + data['incr_point'] + " <br>")
        message.append("**【连续签到天数】**  " + data['cont_count'] + " <br>")
        message.append("**【总签到天数】**  " + data['sum_count'] + " <br>")
        message.append("**【抽奖增加幸运值】**  " + data['draw_lucky_value'] + " <br>")
        message.append("**【总幸运值】**  " + data['total_lucky_value'] + " <br>")
        message.append("**【抽奖结果】**  " + data['lottery_name'] + " <br>")
        message.append("**【矿石总量】**  " + data['sum_point'] + " <br>")
        message.append("![](" + data['lottery_image'] + ") <br>")
    message.append("\n - - - \n")
    return ''.join(message)

# 单条签到
# def checkIn(header):
#     checkin_message = []
#     # 1、签到
#     result_json = _check_in(header)
#
#     requests.get("https://juejin.cn/", headers=header)
#     time.sleep(10)
#     requests.get("https://juejin.cn/user/center/signin?from=main_page", headers=header)
#     time.sleep(10)
#     requests.get("https://juejin.cn/user/center/lottery?from=lucky_lottery_menu_bar", headers=header)
#     time.sleep(10)
#     requests.get("https://juejin.cn/notification", headers=header)
#     time.sleep(10)
#
#     err_no = result_json["err_no"]
#     err_msg = result_json["err_msg"]
#
#     incr_point = 0
#     draw_data = {}
#
#     if err_no != 0:
#         print("check in fail : ", err_msg)
#     else:
#         # 签到成功
#         incr_point = result_json["data"]["incr_point"]
#         draw_data = draw(header)
#     # 获取总矿石
#     sum_point = get_cur_point(header)
#     # 获取连签天数
#     cont_count, sum_count = get_counts(header)
#     # 获取用户头像
#     icon = get_user_icon(header)
#     checkin_message.append("![](" + str(icon) + ") <br>")
#
#     checkin_message.append("**【签到状态码】**  " + str(err_no) + " <br>")
#     checkin_message.append("**【签到信息】**  " + str(err_msg) + " <br>")
#     checkin_message.append("**【获取矿石数】**  " + str(incr_point) + " <br>")
#     checkin_message.append("**【连续签到天数】**  " + str(cont_count) + " <br>")
#     checkin_message.append("**【总签到天数】**  " + str(sum_count) + " <br>")
#     checkin_message.append("**【抽奖增加幸运值】**  " + str(_get(draw_data, 'draw_lucky_value')) + " <br>")
#     checkin_message.append("**【总幸运值】**  " + str(_get(draw_data, 'total_lucky_value')) + " <br>")
#     checkin_message.append("**【抽奖结果】**  " + str(_get(draw_data, 'lottery_name')) + " <br>")
#     checkin_message.append("**【矿石总量】**  " + str(sum_point) + " <br>")
#     checkin_message.append("![](" + str(_get(draw_data, 'lottery_image')) + ") <br>")
#     return ''.join(checkin_message)

# 签到
def _check_in(header):
    result_json = {}
    try:
        # 1、签到
        resp = requests.post(url=_url + '/check_in', headers=header)
        result_json = resp.json()
        print('[_check_in response]', str(result_json))
        resp.close()
    except Exception:
        traceback.print_exc()
        print('_check_in fail')
        result_json['err_no'] = -1
        result_json['err_msg'] = '签到出现异常(灬ꈍ ꈍ灬)'
    return result_json

# 自定义get方法
def _get(obj, name):
    if name not in obj:
        return None
    else:
        return obj[name]

# 签到状态
def get_today_status(header):
    status = False
    msg = None
    try:
        resp = requests.get(url=_url+'/get_today_status', headers=header)
        result_json = resp.json()
        print('[get_today_status response]', str(result_json))
        resp.close()
        if result_json["err_no"] != 0:
            msg = result_json["err_msg"]
            print("get_today_status fail : ", msg)
        else:
            status = result_json["data"]
    except Exception:
        traceback.print_exc()
        print('draw fail')
    return status, msg

# 返回用户头像url
def get_user_icon(header):
    icon = None
    try:
        info_data = get_info(header)
        avatar_large = _get(info_data, 'avatar_large')
        if avatar_large is not None and len(avatar_large) > 0:
            icon = avatar_large[:avatar_large.index("~")] + "~100x100.image"
    except Exception:
        traceback.print_exc()
    return icon

# 获取用户信息
def get_info(header):
    info_data = {}
    try:
        resp = requests.get(url='https://api.juejin.cn/user_api/v1/user/get', headers=header)
        result_json = resp.json()
        resp.close()
        if result_json["err_no"] != 0:
            print("get_info fail : ", result_json["err_msg"])
        else:
            info_data = result_json["data"]
    except Exception:
            traceback.print_exc()
            print('get_info fail')
    return info_data

# 抽奖
def draw(header):
    draw_data = {}
    try:
        resp = requests.post(url=_url+'/lottery/draw', headers=header)
        result_json = resp.json()
        print('[draw response]', str(result_json))
        resp.close()
        if result_json["err_no"] != 0:
            print("draw fail : ", result_json["err_msg"])
        else:
            draw_data = result_json["data"]
    except Exception:
            traceback.print_exc()
            print('draw fail')
    return draw_data

# 获取当天抽奖状态
def get_today_status(header):
    status = True
    try:
        resp = requests.get(url=_url+'/get_today_status', headers=header)
        result_json = resp.json()
        print('[get_today_status response]', str(result_json))
        resp.close()
        if result_json["err_no"] != 0:
            print("get_today_status fail : ", result_json["err_msg"])
        else:
            status = result_json["data"]
    except Exception:
            traceback.print_exc()
            print('get_today_status fail')
    return status

# 获取矿石数
def get_cur_point(header):
    sum_point = None
    try:
        resp = requests.get(url=_url+'/get_cur_point', headers=header)
        result_json = resp.json()
        print('[get_cur_point response]', str(result_json))
        resp.close()
        if result_json["err_no"] != 0:
            print("get_cur_point fail : ", result_json["err_msg"])
        else:
            sum_point = result_json["data"]
    except Exception:
            traceback.print_exc()
            print('get_cur_point fail')
    return sum_point

# 获取签到天数
def get_counts(header):
    cont_count = None
    sum_count = None
    try:
        resp = requests.get(url=_url+'/get_counts', headers=header)
        result_json = resp.json()
        print('[get_counts response]', str(result_json))
        resp.close()
        if result_json["err_no"] != 0:
            print("get_counts fail : ", result_json["err_msg"])
        else:
            cont_count = result_json["data"]["cont_count"]
            sum_count = result_json["data"]["sum_count"]
    except Exception:
            traceback.print_exc()
            print('get_counts fail')
    return cont_count,sum_count
