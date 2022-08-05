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
    sc = "return " + checkin_query
    print(sc)
    resp = driver.execute_script(sc)
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
        if cookie["name"] in ["sessionid", "sessionid_ss"]:
            driver.add_cookie({
                "domain": ".juejin.cn",
                "name": cookie["name"],
                "value": cookie["value"],
                "path": "/",
            })

    driver.get("https://juejin.cn")
    
    WebDriverWait(driver, 240).until(
        lambda x: x.title != "Just a moment..."
    )
    
    driver.get("https://api.juejin.cn/growth_api/v1/check_in")
    
    # resp1 = juejin_checkin(driver)
    # print(resp1)
    # err_no = resp1["err_no"]
    # err_msg = resp1["err_msg"]
    # incr_point = 0
    # sum_point = 0
    # if err_no != 0:
        # print("签到失败：", err_msg)
    # else:
        # incr_point = resp1["data"]["incr_point"]
        # sum_point = resp1["data"]["sum_point"]
    # print(f"签到情况：【状态码】{err_no}【信息】{err_msg}【获取矿石数】{incr_point}【矿石总量】{sum_point}")
    
    # try:
        # if pushplus_token is not None and len(pushplus_token) > 0:
            # message = '签到情况：' + err_msg + '<br/>获取矿石数：' + str(incr_point) + '<br/>总矿石：' + str(sum_point)
            # print('start push message to pushplus:', str(message))
            # title1 = err_msg + ',' + str(incr_point)
            # payload = {'token': pushplus_token, "channel": "wechat", "template": "html", "content": message, "title": title1}
            # resp = requests.post("http://www.pushplus.plus/send", params=payload)
            # print('pushplus code:', resp.status_code)
            # resp.close()
        # else:
            # print('The pushplus_token is none')
    # except Exception:
        # print('push message error')

    #driver.close()
    #driver.quit()

    return 1


pushplus_token = None

if __name__ == "__main__":
    cookie_string = '_ga=GA1.2.1248022175.1657532411; _tea_utm_cache_2608=undefined; __tea_cookie_tokens_2608=%257B%2522web_id%2522%253A%25227119047472190686750%2522%252C%2522user_unique_id%2522%253A%25227119047472190686750%2522%252C%2522timestamp%2522%253A1657532411768%257D; passport_csrf_token=582bc4b6fcfa0dc7fab7a5aac52958a2; passport_csrf_token_default=582bc4b6fcfa0dc7fab7a5aac52958a2; odin_tt=2e012fbc6e39bc1218993239658929110fff40ca127868456abc3fdb75be66a3f2b84782f397d5528f62b227bb415200a13ec1f8d23493a471a5dde52cba662a; n_mh=9-mIeuD4wZnlYrrOvfzG3MuT6aQmCUtmr8FxV8Kl8xY; sid_guard=2cb74f1a7858eb646267e95ab6e45940%7C1657532465%7C31536000%7CTue%2C+11-Jul-2023+09%3A41%3A05+GMT; uid_tt=37c30240c06460d838dde46454ff815a; uid_tt_ss=37c30240c06460d838dde46454ff815a; sid_tt=2cb74f1a7858eb646267e95ab6e45940; sessionid=2cb74f1a7858eb646267e95ab6e45940; sessionid_ss=2cb74f1a7858eb646267e95ab6e45940; sid_ucp_v1=1.0.0-KGYxNDA4NTY2MzhhYTI1OGE2MjgyNmNiMjYyOGQ0ZWY5MzFjZTI3ZTMKFgiNvaDp74yqBRCx4K-WBhiwFDgIQAsaAmxmIiAyY2I3NGYxYTc4NThlYjY0NjI2N2U5NWFiNmU0NTk0MA; ssid_ucp_v1=1.0.0-KGYxNDA4NTY2MzhhYTI1OGE2MjgyNmNiMjYyOGQ0ZWY5MzFjZTI3ZTMKFgiNvaDp74yqBRCx4K-WBhiwFDgIQAsaAmxmIiAyY2I3NGYxYTc4NThlYjY0NjI2N2U5NWFiNmU0NTk0MA; _gid=GA1.2.1392383923.1657706835'
    pushplus_token = ''

    assert cookie_string

    cookie_string = cookie_string.split("&&")
    checkin_codes = list()

    for idx, cookie in enumerate(cookie_string):
        print(f"【Account_{idx + 1}】:")
        checkin_code = juejin(cookie, pushplus_token=pushplus_token)
        checkin_codes.append(checkin_code)

    assert 0 not in checkin_codes, "At least one account login fails."
    assert checkin_codes.count(0) + checkin_codes.count(1) == len(checkin_codes), "Not all the accounts check in successfully."
