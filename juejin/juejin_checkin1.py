# encoding=utf8
import io
import re
import sys
import time
import json
import subprocess
import requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
import os


def get_driver_version():
    cmd = r'''powershell -command "&{(Get-Item 'C:\Program Files\Google\Chrome\Application\chrome.exe').VersionInfo.ProductVersion}"'''
    try:
        out, err = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        out = out.decode('utf-8').split(".")[0]
        return out
    except IndexError as e:
        print('Check chrome version failed:{}'.format(e))
        return 0


def juejin_checkin(driver):
    checkin_url = "https://api.juejin.cn/growth_api/v1/check_in"
    checkin_query = """
        (function (){
        var request = new XMLHttpRequest();
        request.open("POST","%s",false);
        request.setRequestHeader('content-type', 'application/json');
        request.send(null);
        return request;
        })();
        """ % (checkin_url)
    checkin_query = checkin_query.replace("\n", "")
    resp = driver.execute_script("return " + checkin_query)
    resp = json.loads(resp["response"])
    return resp

def juejin(cookie_string, pushplus_token=None):
    options = uc.ChromeOptions()
    options.add_argument("--disable-popup-blocking")

    version = get_driver_version()
    driver = uc.Chrome(version_main=version, options=options)

    # Load cookie
    driver.get("https://juejin.cn")

    if cookie_string.startswith("cookie:"):
        cookie_string = cookie_string[len("cookie:"):]
    cookie_dict = [
        {"name": x[:x.find('=')].strip(), "value": x[x.find('=') + 1:].strip()}
        for x in cookie_string.split(';')
    ]

    driver.delete_all_cookies()
    for cookie in cookie_dict:
        if cookie["name"] in ["koa:sess", "koa:sess.sig"]:
            driver.add_cookie({
                "domain": "glados.rocks",
                "name": cookie["name"],
                "value": cookie["value"],
                "path": "/",
            })

    driver.get("https://juejin.cn")
    WebDriverWait(driver, 240).until(
        lambda x: x.title != "Just a moment..."
    )

    resp1 = juejin_checkin(driver)
    err_no = resp1["err_no"]
    err_msg = resp1["err_msg"]
    incr_point = 0
    sum_point = 0
    if err_no != 0:
        print("签到失败：", err_msg)
    else:
        incr_point = resp1["data"]["incr_point"]
        sum_point = resp1["data"]["sum_point"]
    print(f"签到情况：【状态码】{err_no}【信息】{err_msg}【获取矿石数】{incr_point}【矿石总量】{sum_point}")
    
    try:
        if pushplus_token is not None and len(pushplus_token) > 0:
            message = '签到情况：' + err_msg + '<br/>获取矿石数：' + str(incr_point) + '<br/>总矿石：' + str(sum_point)
            print('start push message to pushplus:', str(message))
            title1 = err_msg + ',' + str(incr_point)
            payload = {'token': pushplus_token, "channel": "wechat", "template": "html", "content": message, "title": title1}
            resp = requests.post("http://www.pushplus.plus/send", params=payload)
            print('pushplus code:', resp.status_code)
            resp.close()
        else:
            print('The pushplus_token is none')
    except Exception:
        print('push message error')

    driver.close()
    driver.quit()

    return err_no


pushplus_token = None

if __name__ == "__main__":
    cookie_string = sys.argv[1]
    pushplus_token = os.environ['PUSHPLUS_TOKEN']

    assert cookie_string

    cookie_string = cookie_string.split("&&")
    checkin_codes = list()

    for idx, cookie in enumerate(cookie_string):
        print(f"【Account_{idx + 1}】:")
        checkin_code = juejin(cookie, pushplus_token=pushplus_token)
        checkin_codes.append(checkin_code)

    assert 0 not in checkin_codes, "At least one account login fails."
    assert checkin_codes.count(0) + checkin_codes.count(1) == len(checkin_codes), "Not all the accounts check in successfully."
