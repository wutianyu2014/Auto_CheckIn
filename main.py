# encoding=utf8
from juejin import *
from push_message import *
from util import *
import os

group_id = 'ABC123'

if __name__ == '__main__':
    # # glados平台cookie
    juejin_cookie = os.environ['JUEJIN_COOKIE']
    # pushplus平台token
    pushplus_token = os.environ['PUSHPLUS_TOKEN']

    send_message = []

    checkin_message = juejin_checkIn(juejin_cookie)

    title = None

    # 增加彩虹屁
    if len(checkin_message) > 0:
        title = get_rainbow_text()
        if title is not None and len(title) > 0:
            send_message.append(f">## {title} \n\n")
        send_message.append(''.join(checkin_message))

    message = ''.join(send_message)

    # 第一次推送
    msg = pushplus_message(pushplus_token, title, message, group_id)
    if msg is not None:
        # 推送失败再次推送
        time.sleep(10)
        pushplus_message(pushplus_token, '再次推送,首次推送失败:' + msg, message, group_id)
