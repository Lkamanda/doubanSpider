import sys
from bs4 import BeautifulSoup
import time
import requests
import time
from openpyxl import Workbook
import numpy as np
from urllib import request, error
import random

# Some User Agents
heads = [
    {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'},
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0'}
]

def book_spider(book_tag):
    page_num = 0
    book_list = []
    try_times = 0
    while(1):
        url = 'http://www.douban.com/tag/%E5%B0%8F%E8%AF%B4/book?start=0'
        # url = 'https://www.douban.com/tag/%E5%B0%8F%E8%AF%B4/' + '/book?start=' + str(page_num * 15)
        time.sleep(3)
        # time.sleep(random.randint(5))
        try:
            req = requests.get(url=url, headers=heads[random.randint(0, 3)])
            source_code = req.text
            plain_text = str(source_code)
        except error.HTTPError as e:
            print(e)
            continue
        except error.URLError as e:
            print(e)
            continue

        soup = BeautifulSoup(plain_text)
        list_soup = soup.find('div', {'class': "mod book-list"})
        try_times += 1

        # 加入程序停止判断
        if list_soup == None and try_times < 200:
            continue
        elif list_soup == None or len(list_soup) <= 1:
            break
        for book_info in list_soup('dd'):
            title = book_info.find('a', {'class':'title'}).string.strip()
            desc = book_info.find('div', {'class':'desc'}).string.strip()
            # 去掉str中的'/'
            desc_list = desc.split('/')
            book_url = book_info.find('a', {'class':'title'}).get('href')

            # 获取数据
            try:
                author_info = '作者译者: ' + '/'.join(desc_list[0:-3])
            except:
                author = '作者/译者： 暂无'
            try:
                pub_info = '出版信息：' + '/'.join(desc_list[-3:0])
            except:
                pub_infor = '出版信息：暂无'
            # 获取书的评分
            try:
                ranting = book_info.find('span',{'class':'rating_nums'})
            except:
                ranting = '0.0'
            # 通过book_url内的网址,进入书的详情页面获取信息

def get_people_num(url):
    # https://book.douban.com/subject/6518605/?from=tag_allc  # for test
    global plain_text
    try:
        req = requests.get(url, headers=heads[random.randint(0, 3)])
        source_code = req.text
        plain_text = str(source_code)
    except error.HTTPError as e:
        print(e)
    except error.URLError as e:
        print(e)
    soup = BeautifulSoup(plain_text, 'html.parser')    # 解释器： html.parse
    people_num = soup.find('div', {'class': 'rating_sum'}).findAll('span')[1].string.strip()
    # print(people_num)
    return people_num
if __name__ == '__main__':
    book_spider()
