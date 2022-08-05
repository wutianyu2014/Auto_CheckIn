# encoding=utf8
import traceback
import time

from juejin import *
from push_message import *

split_str = '&@@&'

if __name__ == '__main__':
    # glados平台cookie
    juejin_cookie = os.environ['JUEJIN_COOKIE']
    # pushplus平台token
    pushplus_token = os.environ['PUSHPLUS_TOKEN']

    checkin_message = []

    # juejin执行签到
    if juejin_cookie is not None and len(juejin_cookie) > 0:
        juejin_cookie = juejin_cookie.split(split_str)
        # 遍历cookie执行签到，并返回签到状态码和签到信息
        for idx, cookie in enumerate(juejin_cookie):
            time.sleep(10)
            print(f"[juejin_Account_{idx + 1}]:")
            juejin_result = juejin_checkIn(cookie)
            # 存在账户签到信息，说明成功执行了签到
            checkin_message.append(f">### juejin_Account_{idx + 1} checkin message\n" + str(juejin_result) + "\n - - - \n")

    # 所有账号签到完毕，判断是否有签到信息，如果有签到信息说明账号执行了签到
    if checkin_message is not None and len(checkin_message) > 0:
        try:
            # 推送签到消息至pushplus平台
            if pushplus_token is not None and len(pushplus_token) > 0:
                pushplus_message(pushplus_token, ''.join(checkin_message), "ABC123")
            else:
                print('The pushplus_token is none')
        except Exception as e:
            traceback.print_exc()
            print('push message error')