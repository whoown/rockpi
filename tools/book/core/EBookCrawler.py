# coding=utf-8
# -*- coding: UTF-8 -*-
__author__ = 'Rock'
import requests

site_host = "http://desk.zol.com.cn/pc/%(page_id)d.html"
host = "http://desk.zol.com.cn"
site_url = "http://www.allmacwallpaper.com/mac-wallpapers/Date/%(page_id)d?home=1"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
    'Host': 'www.wenku8.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate'}

session = requests.Session()
session.headers.update(headers)

load_session = requests.Session()
load_headers = headers.copy()
print(load_headers)
load_headers['Host'] = "b.zol-img.com.cn"
load_session.headers.update(load_headers)


class EBookCrawler:
    def __init__(self):
        pass

    def create_chapter(self, chapter_title, chapter_url):
        return None

    def create_book(self):
        return None

    def create_series(self, series_url, specific_series_name=''):
        return None

