import csv
import json
from bs4 import BeautifulSoup


def get_whole_text_url(element):
    '''
    获取完整博文的url
    :param element: 获取url得到的每个element
    :return: 完整博文的url
    '''
    # @click方法处的内容
    url_selector = element.get('@click')
    #https://weibo.com/5704916395/Nma0HEPmV?refer_flag=1001030103_
    complete_url = url_selector.split("'")[1]
    #根据完整微博链接中信息构建api
    target_id = complete_url.split('/')[-1].split('?')[0]

    # 通过高级搜索结果获得对应博文的api
    # https://weibo.com/ajax/statuses/show?id=Nma0btuis&locale=zh-CN
    complete_url = f'https://weibo.com/ajax/statuses/show?id={target_id}&locale=zh-CN'

    return complete_url


def get_weibo_info(js_text):
    '''
    根据评论api获取的json格式文本读取评论相关信息
    :param js_text:
    :return:
    '''
    try:
        time = js_text['created_at']    # 发布时间
    except:
        time = ""

    try:
        weibo_id = js_text['id']        # 微博id
    except:
        weibo_id = ""

    try:
        user_name = js_text['user']['screen_name'] # 用户名称
    except:
        user_name = ""

    try:
        user_id = js_text['user']['id'] # 用户id
    except:
        user_id = ""

    try:
        text_raw = js_text['text_raw'] # 微博文本
    except:
        text_raw = ""

    try:
        region = js_text['region_name']    # ip所属地
    except:
        region = ""

    reposts_count = js_text['reposts_count'] # 转发数
    comments_count = js_text['comments_count'] # 评论数
    attitudes_count = js_text['attitudes_count'] # 表态数
    attitudes_status = js_text['attitudes_status'] # 表态倾向

    # 评论api
    comment_api = f'https://weibo.com/ajax/statuses/buildComments?is_reload=1&id={weibo_id}&is_show_bulletin=2&is_mix=0&count=10&uid={user_id}&fetch_level=0&locale=zh-CN'

    weibo_dict = {'created_time': time,
                  'weibo_id':weibo_id,
                  'user_name':user_name,
                  'uid':user_id,
                 'text':text_raw,
                 'region':region,
                 'repost_count':reposts_count,
                 'comments_count':comments_count,
                 'attitudes_count':attitudes_count,
                 'attitudes_status':attitudes_status,
                  'comment_api':comment_api
                 }


    return weibo_dict


def get_comments(js_text):
    data = js_text['data']
    comments_ls = []
    for item in data:
        comment = {}
        time = '' + item['created_at']
        id = '' + item['idstr']
        source = '' + item['source']
        user_name = '' + item['user']['screen_name']
        user_id = '' + item['user']['idstr']
        text = '' + item['text_raw']
        like_counts = item['like_counts']
        comment['created_time'] = time
        comment['id'] = id
        comment['source'] = source
        comment['user_name'] = user_name
        comment['uid'] = user_id
        comment['text'] = text
        comment['like_counts'] = like_counts
        comments_ls.append(comment)
    return comments_ls

def get_user_info(html_text):

    js_text = json.loads(html_text)
    info = js_text['data']['user']
    # uid
    uid = info['idstr']
    # user id
    screen_name = info['screen_name']
    # 认证类型
    verified_type = info['verified_type']
    # 描述
    description = info['description']
    # 性别
    gender = info['gender']
    # 粉丝数
    followers_count = info['followers_count']
    # 关注数
    friends_count = info['friends_count']
    # 微博数
    statuses_count = info['statuses_count']
    # 用户类型（黄V，蓝V之类）
    user_type = info['user_type']
    # 领域
    try:
        domain = info['domain']
    except:
        domain = ''
    # 认证理由
    try:
        verified_reason = info['verified_reason']
    except:
        verified_reason = ''

    user_info_dict = {
        'uid': uid,
        'screen_name': screen_name,
        'verified_type': verified_type,
        'description' : description,
        'gender':gender,
        'followers_count': followers_count,
        'friends_count' : friends_count,
        'statuses_count' : statuses_count,
        'user_type' : user_type,
        'domain' : domain,
        'verified_reason' : verified_reason
    }

    return user_info_dict




if __name__ == '__main__':
    st = 'SINAGLOBAL=2222304490476.865.1659447375345; UOR=,,login.sina.com.cn; _s_tentry=-; Apache=8487210593750.496.1697869911380; ULV=1697869911382:6:1:1:8487210593750.496.1697869911380:1683796681464; XSRF-TOKEN=e4L0EmeFJ4KAV7nKMYCCBbcF; SSOLoginState=1697870081; MEIQIA_TRACK_ID=2X4FoAp58KjvPWGtKnnPw8m0GJd; MEIQIA_VISIT_ID=2X4FoJ8EAkvcXiC3aiQGnSXN3Dm; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWiuGG9kWaKNw3DIVgZ6nIi5JpX5KMhUgL.FoMRSoB7Sh-c1h22dJLoI74jIgpDqcvkqfv.9PS4d7tt; SCF=AqjQIFlXNAHGkHgBkET9xDQwPyNNdMdaaNU5PiVG4DbRIrsPfqsXAQ4HynryWk61qPdft8aSoZTgpQ_9Y3ZYKuI.; SUB=_2A25IMLL3DeRhGeFG7VYR9CvKwz2IHXVrR6M_rDV8PUNbmtAGLRDhkW9NeQoDl4k_Iu-5WUpVOl6SzIC2jhbZ8sI-; ALF=1700548519; PC_TOKEN=ddb1bd8379; WBPSESS=yYmIz0OECWt95NmiZe7cbbIGvYk8HFcLuPVxAofV6eK_IOlLBffNtpIpazSCYXHEHyOAKrhuRKvWiEQdU815FLrEpU29vLisRBT02ExwkuxEmQA0dZoXxXJJodINVuHBtwqY7J49DW4ObkNDFsUxhg=='
    rst = st.split(";")
    rsls = [r.split("=") for r in rst]
    dic = {}
    for rs in rsls:
       dic[rs[0].strip()] = rs[1].strip()
    print(dic)
