import urllib.request
import re
import threading
from bs4 import BeautifulSoup
import os
import time

siteURL = "http://www.umei.cc/p/gaoqing/cn/"
u = []

def getPageContent(url):  # 获取页面内容
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    return response


def getListUrl():  # 获取每个套图的地址
    urls = []
    page_content = getPageContent(siteURL)
    soup = BeautifulSoup(page_content, 'lxml').find('div', class_='TypeList').find_all('a',
                                                                                       attrs={
                                                                                           "class": "TypeBigPics"})
    loops = range(len(soup))
    # for j in loops:
    #     t=threading.Thread(target=soup[j].get, args=('href',))
    for i in soup:
        url = i.get('href')
        urls.append(url)
    return urls


def getPageNums(url):  # 获取套图总的页码数
    page_content = getPageContent(url)
    soup = BeautifulSoup(page_content, 'lxml').find('div', class_='NewPages').find('a').text
    nums = re.findall("\d+", soup)[0]
    return nums


def getImgUrl(url):  # 获得每个套图每张照片的地址列表
    page_nums = int(getPageNums(url))
    pp = getPageContent(url)
    # print(type(page_nums))
    path = BeautifulSoup(pp, 'lxml').find('title').text
    mkdir(path)
    os.chdir(os.path.join("D:\mzitu", path))
    url_fix = url.replace('.htm', '')
    print(url_fix)
    urls = []
    for i in range(1, page_nums):
        img_u = url_fix + '_' + str(i) + '.htm'
        # print(img_u)
        page_content = getPageContent(img_u)
        img_info = BeautifulSoup(page_content, 'lxml').find('div', class_='ImageBody').find('img')
        img_url = img_info.get('src')  # 获当前图片地址
        # self.save(img_url) #循环中保存形成阻塞
        u.append(img_url)
    return 0


def save(img_url):  # 保存图片
    name = img_url.replace('http://i1.umei.cc/uploads/tu/', '')
    name2 = name.replace('/', '_')
    print(img_url)
    img = urllib.request.urlopen(img_url)
    data = img.read()
    print('hahha')
    f = open(name2 + '.jpg', 'ab')
    f.write(data)
    print('xxxx')
    f.close()


def mkdir(path):  # 这个函数创建文件夹
    isExists = os.path.exists(os.path.join("D:\mzitu", path))
    if not isExists:
        print(u'建了一个名字叫做', path, u'的文件夹！')
        os.makedirs(os.path.join("D:\mzitu", path))
        os.chdir(os.path.join("D:\mzitu", path))  ##切换到目录
        return True
    else:
        print(u'名字叫做', path, u'的文件夹已经存在了！')
        return False


def main():
    item = getListUrl()
    # print(item)
    loops = range(len(item))
    threadss = []
    for i in loops:
        t = threading.Thread(target=getImgUrl, args=(item[i],))
        threadss.append(t)

    for i in loops:
        threadss[i].start()

    for i in loops:
        threadss[i].join()

    threads = []
    nloops = range(len(u))

    for i in nloops:
        t = threading.Thread(target=save, args=(u[i],))
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()


if __name__ == '__main__':
    main()
