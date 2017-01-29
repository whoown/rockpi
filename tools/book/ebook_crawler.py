# coding=utf-8
# -*- coding: UTF-8 -*-
import urlparse

from core.Wenku8Crawler import Wenku8Crawler

__author__ = 'Rock'

DEFAULT_DIR = "/Users/zhangyan/Desktop"
BOOK_SITES = {'www.wenku8.com': Wenku8Crawler}


def get_book(url, save_path=DEFAULT_DIR, specific_series_name=''):
    if not url or not save_path:
        return
    host = urlparse.urlparse(url).netloc
    clz = BOOK_SITES.get(host)
    if not clz:
        print 'No crawler for : ', host
        return
    crawler = clz()
    series = crawler.create_series(url, specific_series_name)
    if series:
        series.save_to_txt(save_path)


if __name__ == '__main__':
    get_book("http://www.wenku8.com/novel/1/1213/index.htm")
