import json
import requests
import csv
import time
from lxml import etree
from bs4 import BeautifulSoup
from funcs import get_whole_text_url, get_weibo_info,get_comments, get_user_info


def get_html_text(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        "Referer": "https://weibo.com"
    }


    cookies = {'SINAGLOBAL': '2222304490476.865.1659447375345',
               'UOR': ',,login.sina.com.cn',
               '_s_tentry': '-',
               'Apache': '8487210593750.496.1697869911380',
               'ULV': '1697869911382:6:1:1:8487210593750.496.1697869911380:1683796681464',
               'XSRF-TOKEN': 'e4L0EmeFJ4KAV7nKMYCCBbcF',
               'SSOLoginState': '1697870081',
               'MEIQIA_TRACK_ID': '2X4FoAp58KjvPWGtKnnPw8m0GJd',
               'MEIQIA_VISIT_ID': '2X4FoJ8EAkvcXiC3aiQGnSXN3Dm',
               'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9W5_mZyOb9YEfj-9BL6MPvBF5JpX5KzhUgL.FoMfShBXeoB0ShM2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNSKBXShzXe0BN',
               'SCF': 'AqjQIFlXNAHGkHgBkET9xDQwPyNNdMdaaNU5PiVG4DbRde5-WCqBvfDI0khVDBj0Qayj7O041MrRjBuYngmEGt4.', # changed
               'SUB': '_2A25IOauPDeThGeFL71YV8irPzzuIHXVrTppHrDV8PUNbmtAGLXHSkW9NQgXCX0SZJFrIcJoNhVgDUC6HuLazFlNU', # changed
               'ALF': '1730088799', # changed
               'PC_TOKEN': '2f5776d028',
               'login_sid_t':'6739f8bac9b9911b8a05948c7fd1bc3e',
               'WBPSESS': '0-1ZuBczdfUPEtAIqAPhFMSvgw0N35z-js2yu6-4tqNCPQxrCpXBXY6jzG9YeGTmalOv0CbYnlno9Y5kofgpyW2kcDI14sEjzvpK2p7uPoPhOr4BfFu4P3i54g4Ev5LChBJnwUnPZQaC8xLHOghIgQ=='
               }

    rq = requests.get(url, headers=headers, cookies=cookies)
    # 修改编码
    rq.encoding = 'utf8'
    time.sleep(1)  # 加上3s 的延时防止被反爬
    # 还原成网页源码的形式
    #print(rq.text)
    return rq.text






def main(keyword, start_time, end_time):
    page=1 # 初始页面：第一页

    headers = ['created_time', 'weibo_id', 'user_name', 'uid', 'text', 'region', 'repost_count',
               'comments_count', 'attitudes_count', 'attitudes_status','comment_api']

    while True:
        print(f'------------------Processing Page {page}------------------')
        # https://s.weibo.com/weibo?q=%E6%B3%B0%E5%9B%BD%E6%9E%AA%E5%87%BB&typeall=1&suball=1&timescope=custom%3A2023-10-03-16%3A2023-10-03-18&Refer=g
        url = f"https://s.weibo.com/weibo?q={keyword}&scope=ori&typeall=1&suball=1&timescope=custom%3A{start_time}%3A{end_time}&Refer=g&page={page}"
        print(url)
        html_text = get_html_text(url)
        soup = BeautifulSoup(html_text, 'html.parser')

        # 获取该页面的内容
        text_selector = "#pl_feedlist_index > div:nth-child(2) > div > div > div.card-feed > div.content "
        raw_texts = soup.select(text_selector)
        url_selector = "div.info > div > ul > li > a"

        # 若页面没内容了就退出
        if len(raw_texts) == 0:
            break
        if page > 50:
            break

        for raw_text in raw_texts:
            raw_url = raw_text.select(url_selector)[-1]
            api = get_whole_text_url(raw_url)
            print(f"   {api}")
            # 获取api里面的数据
            rq_text = get_html_text(api)
            js_weibo = json.loads(rq_text)
            dict_weibo = get_weibo_info(js_weibo)

            print(dict_weibo)

            with open('Blogs.csv', 'a+') as f:
                dw = csv.DictWriter(f, fieldnames=headers)
                dw.writerow(dict_weibo)

        page += 1

def user_main():
    with open('uid.csv', 'r') as f:
        uids = f.readlines()
    uids = uids[1:]

    headers = ['uid','screen_name','gender','followers_count','friends_count','statuses_count','verified_type','verified_reason','description','user_type','domain']

    # 3832
    for uid in uids[3825:3832]:
        uid = uid.strip()
        url = f'https://weibo.com/ajax/profile/info?custom={uid}'

        html_text = get_html_text(url)
        user_info = get_user_info(html_text)

        print(user_info)

        with open('Users.csv', 'a+') as f:
            dw = csv.DictWriter(f, fieldnames=headers)
            dw.writerow(user_info)


if __name__ == '__main__':
    user_main()


