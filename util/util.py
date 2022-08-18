import requests
import traceback

# 彩虹屁
def get_rainbow_text():
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