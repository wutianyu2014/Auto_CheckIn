# encoding=utf8
from juejin import *
from push_message import *
import os

if __name__ == '__main__':
    # # glados平台cookie
    juejin_cookie = os.environ['JUEJIN_COOKIE']
    # pushplus平台token
    pushplus_token = os.environ['PUSHPLUS_TOKEN']

    checkin_message = juejin_checkIn(juejin_cookie)

    pushplus_message(pushplus_token, ''.join(checkin_message), 'ABC123')