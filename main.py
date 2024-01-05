# encoding=utf8
from juejin import *
from push_message import *
from util import *
import os

group_id = 'ABC123'

def checkin():
    # # glados平台cookie
    juejin_cookie = os.environ['JUEJIN_COOKIE']

    # pushplus平台token
    pushplus_token = os.environ['PUSHPLUS_TOKEN']

    result_list = batch_checkIn(juejin_cookie)
    if len(result_list) <= 0:
        return None

    send_message = []

    title, content = get_send_content(result_list)

    # 增加彩虹屁
    rainbow = get_rainbow_text()

    if rainbow is not None and len(rainbow) > 0:
        send_message.append(f">## {rainbow} \n\n")
        if len(title) == 0:
            # 全部签到成功 标题替换成彩虹屁
            title = rainbow

    send_message.append(content)
    message = ''.join(send_message)

    # 第一次推送
    msg = pushplus_message(pushplus_token, title, message, None)
    # if msg is not None:
    #     # 推送失败再次推送
    #     time.sleep(10)
    #     pushplus_message(pushplus_token, '再次推送,首次推送失败:' + msg, message, None)

if __name__ == '__main__':
    checkin()
