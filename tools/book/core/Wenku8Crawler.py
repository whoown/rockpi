# coding=utf-8
# -*- coding: UTF-8 -*-
import re

import requests
from bs4 import BeautifulSoup, Tag

from tools.book.core.EBookCrawler import EBookCrawler
from tools.book.core.Models import Series, Book, Chapter

__author__ = 'Rock'

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
load_headers['Host'] = "b.zol-img.com.cn"
load_session.headers.update(load_headers)


class Wenku8Crawler(EBookCrawler):
    def create_chapter(self, chapter_title, chapter_url):
        ret = session.get(chapter_url)
        html_text = unicode(ret.content, 'gbk')
        soup = BeautifulSoup(html_text, "html.parser")

        if not chapter_title:
            title_div = soup.find("div", {'id': 'title'})
            if title_div:
                chapter_title = title_div.string.strip()
        chapter = Chapter(chapter_title)

        content = soup.find("div", {'id': 'content'}).contents
        for c in content:
            if isinstance(c, Tag) or len(c.string.strip()) == 0:
                continue
            chapter.append_line(c.string.strip())

        print 'create chapter name:[%s], length:[%d]' % (chapter.title, len(chapter.content))

        return chapter

    def create_book(self):
        return None

    def create_series(self, series_url, specific_series_name=''):
        try:
            ret = session.get(series_url)
        except Exception, e:
            print 'Fail to create series since:', e
            return None
        html_text = unicode(ret.content, 'gbk')
        soup = BeautifulSoup(html_text, 'html.parser')
        body = soup.find("body")
        series_title = body.find("div", {'id': 'title'}).string.strip()
        series_title = re.sub(u"\(.+\)", '', series_title)
        if specific_series_name:
            series_title = specific_series_name
        series_infos = body.find("div", {'id': 'info'}).string.strip()
        series_author = ''
        match_auther = re.search(u"作者[:：](.+)\s*", series_infos)
        if match_auther and match_auther.group(1):
            series_author = match_auther.group(1)

        print 'create series name:[%s], author:[%s]' % (series_title, series_author)

        catalog_table = body.find("table")
        tr_list = catalog_table.find_all("tr")
        books = []
        book_name = ''
        book_chapters = []
        for tr in tr_list:
            if tr.find("td", {'class': 'vcss'}):  # This row is headline
                if book_name:
                    books.append((book_name, book_chapters))
                book_name = tr.find("td").string.strip()
                book_chapters = []
            else:
                tds = tr.find_all("a")
                for a in tds:
                    book_chapters.append((a.get('href'), a.string.strip()))
        if book_name:
            books.append((book_name, book_chapters))

        series = Series(series_title, series_author)

        for b in books:
            book = Book(b[0], series_author)
            print '===== create book name:[%s] =====' % b[0]
            for c in b[1]:
                chapter_url = re.sub("index.htm", c[0], series_url)
                chapter = self.create_chapter(c[1], chapter_url)
                book.add_chapter(chapter)
            series.add_book(book)

        return series
