# encoding=utf8
from juejin import *
from push_message import *
import os

# 彩虹屁
def get_text():
    try:
        resp = requests.get(url='https://api.shadiao.pro/chp')
        result_json = resp.json()
        print('[get_text response]', str(result_json))
        resp.close()
        if resp.status_code == 200:
            return result_json['data']['text']
    except Exception:
        traceback.print_exc()
        print('get_text fail')
    return None

if __name__ == '__main__':
    # # glados平台cookie
    juejin_cookie = os.environ['JUEJIN_COOKIE']
    # pushplus平台token
    pushplus_token = os.environ['PUSHPLUS_TOKEN']

    send_message = []

    checkin_message = juejin_checkIn(juejin_cookie)

    # 增加彩虹屁
    if len(checkin_message) > 0:
        text = get_text()
        if text is not None and len(text) > 0:
            send_message.append(f">## {text} \n\n")
        send_message.append(''.join(checkin_message))

    message = ''.join(send_message)

    pushplus_message(pushplus_token, message,  'ABC123')