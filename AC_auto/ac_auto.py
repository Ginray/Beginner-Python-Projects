# -*- coding=utf-8  -*-

import cookielib
import threading
import urllib

import re

import time

import requests
from  bs4 import BeautifulSoup
import sys
import urllib2

global username,password

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER'
}


language={  'g++':'0',
            'gcc':'1',
            'c++':'2',
            'c':'3',
            'pascal':'4',
            'java':'5',
            'c#':'6',
            'cpp':'0'

}

start_pro = 1000
end_pro = 5000


def login():

    username=raw_input("please input username:\n")
    password=raw_input("please input password:\n")
    # type: () -> object

    login_info={
        'username':username.strip(),
        'userpass':password.strip(),
    }

    hdu_url = 'http://acm.hdu.edu.cn/userloginex.php?action=login'

    login_info=urllib.urlencode(login_info)

    co= cookielib.LWPCookieJar()
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(co))

    hdu_session=urllib2.Request(hdu_url,login_info,headers)
    try:
        loginin=opener.open(hdu_session).read()
    except:
        print'请检查网络是否联通'


    if(loginin.find('No such user or wrong password.')!=-1):
        print 'No such user or wrong password.'
        exit()

    headers['Cookie'] = re.search('PHPSESSID=[A-Za-z0-9_]*', str(co)).group()  # 提取cookie
    print 'Login success'

    return



def status (pro_id):
    global qian_id, headers
    status_url = 'http://acm.hdu.edu.cn/status.php?user=' + qian_id
    req = urllib2.Request(status_url, urllib.urlencode({}), headers)

    while(True):
        time.sleep(1)

        html=urllib2.urlopen(req).read()
        soup=BeautifulSoup(html,'lxml')
        for i in soup.table.find_all('table')[-2].find_add('tr'):
            ans=i.find_all['td']
            if(ans[3].string==pro_id):
                dan=ans[2].string
                if(dan!='Queuing'and dan!='Comiling'):
                    print dan
                    return
                break

def find_the_code_path(pro_id, url_path):  # 搜索代码路径
    print 'start ' + pro_id
    find_code_url = url_path(pro_id)
    for i in find_code_url:
        print 'find in ' + i
        find_the_code(i, pro_id)
        time.sleep(10)


def find_the_code(url, pro_id):  # 寻找页面内代码并提交
    global headers

    # POST
    submit_url = 'http://acm.hdu.edu.cn/submit.php?action=submit'

    sesson = requests.Session()
    sesson.headers.update(headers)

    try:
        html_code = sesson.get(url).text

        soup = BeautifulSoup(html_code, "lxml")  # 美味的汤

        for i in soup.find_all('pre'):
            code = i.string  # 最终代码

            if code == None:
                return

            try:
                if (code.find('main') != -1):  # 如果代码中有main函数
                    # POST数据
                    post_data = {
                        'problemid': pro_id,
                        'usercode': code,
                        'language': language[i.get('class')[0]]
                    }
                    # 需要给Post数据编码
                    postData = urllib.urlencode(post_data)
                    request = urllib2.Request(submit_url, postData, headers)
                    print 'post ' + pro_id
                    urllib2.urlopen(request)
                    # status(pro_id)
                    f=open('ac.txt','a+')
                    f.write(pro_id+'  ')
                    f.close()
                    print '------------------ ' + pro_id + ' Submit successfully\n'
            except KeyError, TypeError:
                print 'KeyError'

    except urllib2.URLError:  # 异常情况
        print 'URLError'


def from_baidu(pro_id):
    find_path = 'http://www.baidu.com/s?&wd=HDU%20' + pro_id + '%20CSDN'  # 百度
    baidu_code = urllib2.urlopen(find_path).read()
    find_code_url = re.findall('(http://www.baidu.com/link\?url=[^\"]*)', baidu_code)
    return find_code_url[:3]


def start():  # 单线程
    for i in range(start_pro, end_pro):
        pro_id = str(i)
        find_the_code_path(pro_id, from_baidu)  # 从百度

def start2():  # 多线程
    for i in range(start_pro, end_pro, 3):
        f = open('ac.txt','a+')
        ac_log=f.read()
        f.close()
        if ac_log.find(str(i))!=-1:
            continue

        threads = []
        for j in range(i, i + 3):
            pro_id = str(j)
            threads.append(threading.Thread(target=find_the_code_path, args=(pro_id, from_baidu)))  # 从百度

        if len(threads) == 0:  # 如果返回为空
            continue
        for t in threads:
            t.setDaemon(True)
            t.start()
            time.sleep(5)
        t.join()
    print "All over"


if __name__ == '__main__':
    reload(sys)
    login()
    start2()