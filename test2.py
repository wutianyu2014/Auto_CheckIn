# encoding=utf8

import requests
from bs4 import BeautifulSoup
import time

split_str = '&@@&'

headers = {
        'Connection': 'close',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/json;charset=UTF-8',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                      " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "Referer": "https://juejin.cn/",
        "Accept-Encoding": "gzip, deflate",
    }

def get_info(url):
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    ranks = soup.select('span.pc_temp_num')
    titles = soup.select('div.pc_temp_songlist > ul > li > a')
    times = soup.select('span.pc_temp_tips_r > span')
    for rank, title, time in zip(ranks, titles, times):
        data = {
            'rank': rank.get_text().strip(),
            'singer': title.get_text().split('-')[0],
            'song': title.get_text().split('-')[0],
            'time': time.get_text().strip()
        }
        print(data)

if __name__ == '__main__':
    get_info('http://www.kugou.com/yy/rank/home/1-8888.html')
    # urls = ['http://www.kugou.com/yy/rank/home/{}-8888.html'.format((str(i)) for i in range(1, 24))]
    # print(urls)
    # for url in urls:
    #     get_info(url)
    #     time.sleep(1)