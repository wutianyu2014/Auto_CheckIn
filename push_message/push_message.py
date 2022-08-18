import requests
import traceback

# 推送签到消息至pushplus平台
def pushplus_message(token, title, message, topic):
    # token为空
    if token is None or len(token) <= 0:
        print('The pushplus_token is none')
        return
    # 推送消息为空
    if message is None or len(message) <= 0:
        print('The message is none')
        return

    # 推送消息
    try:
        payload = {'token': token, "channel": "wechat", "template": "markdown", "content": message,
                   "title": "checkin status"}
        if topic is not None:
            payload["topic"] = topic
        if title is not None:
            payload["title"] = str(title[0:30] + '...').replace('\n', ' ')
        resp = requests.post("http://www.pushplus.plus/send", params=payload)
        print('pushplus response:', str(resp.json()))
        resp.close()
    except Exception:
        traceback.print_exc()
        print('push message error')



def server_messgae(token, title, message):
    payload = {"title": title, "desp": message, }
    resp = requests.post(f"https://sctapi.ftqq.com/{token}.send", params=payload)
    result = resp.json()
    if result["code"] == 0:
        print("Push the message to server success(code:0),the code is:" + str(result["code"]))
    if result["code"] != 0:
        print("Push the message to server error(code!=0),The error message is " + str(result["code"]) + str(result["message"]))
    code = resp.status_code
    resp.close()
    return code
