# encoding=utf8

import requests
from bs4 import BeautifulSoup
import time
import re

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
    soup = BeautifulSoup(wb_data.text, 'html.parser')
    ranks = soup.select('span.pc_temp_num')
    titles = soup.select('div.pc_temp_songlist > ul > li > a')
    times = soup.select('span.pc_temp_tips_r > span')
    # print(soup)
    datas = []
    for rank, title, time in zip(ranks, titles, times):
        data = {
            'rank': rank.get_text().strip(),
            'singer': title.get_text().split('-')[1].strip(),
            'song': title.get_text().split('-')[0].strip(),
            'time': time.get_text().strip(),
            'url': re.findall('href="(.*?)"', str(title))[0]
        }
        datas.append(data)
    return datas

def get_music_id(url):
    req = requests.get(url, headers=headers)
    # print(req.text)
    hash_list = re.findall('"hash":"(.*?)"', req.text)
    album_id_list = re.findall('"album_id":(\d+),', req.text)
    music_id_list = zip(hash_list, album_id_list)
    # print(hash_list)
    # print(album_id_list)
    return music_id_list

def get_music_info(hash, album_id):
    url = f'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash={hash}&dfid=1Jd2vy2B39ve4ZWgxr0kXsNh&appid=1014&mid=78938e2b2b0feb7afd1c69e6b318972d&platid=4&album_id={album_id}&_=1661352113708'
    req = requests.get(url, headers=headers)
    # pprint.pprint(req.json())
    title = req.json()['data']['audio_name']
    play_url = req.json()['data']['play_url']
    music_info = [title, play_url]
    return music_info

def save(title, play_url):
    music_content = requests.get(play_url, headers=headers).content
    with open('C:\\Users\\wutianyu\\Music\\py1\\' + title + '.mp3', mode='wb') as f:
        f.write(music_content)

if __name__ == '__main__':
    # 第几页
    i = 2
    url = 'http://www.kugou.com/yy/rank/home/{}-8888.html'.format((str(i)))
    datas = get_info(url)
    for d in datas:
        print(d)
        music_id_list = get_music_id(d['url'])
        for hash_list, album_id_list in music_id_list:
            music_info = get_music_info(hash_list, album_id_list)
            print(str(music_info))
            save(music_info[0], music_info[1])