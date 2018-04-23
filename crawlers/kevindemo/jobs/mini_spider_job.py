# -*- coding: utf-8 -*-
"""
Created on Sun Apr 08 10:55:25 2018

@author: shenchao05
https://www.cnblogs.com/feeland/p/4514771.html
"""

import requests
from bs4 import BeautifulSoup

from utils import logger
from utils import strtools, filetools
from inspect import isfunction
import urlparse


class MiniSpiderJob:
    url = None
    depth = 0
    _timeout = 60
    _save_dir = None
    _exec_cbk = None

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'}

    def __init__(self, url, save_dir, timeout, depth, callback):
        self.url = url
        self._save_dir = save_dir
        self._executing = False
        self._timeout = timeout if 0 < timeout < 60 * 60 else 60
        self.depth = depth
        self._exec_cbk = callback

    # 执行此单一爬虫任务，包括：1. 网页HTTP请求+重试机制 2. 解析网页获取所有<a>标签  3. 保存网页到指定目录  4. 最后调用Callback
    def execute(self):

        print 'Job Execute ', self.url
        response = self._make_request(3)
        if not response or response.status_code != 200:
            Logger.log("[SpiderJob] request failed. response: %s" % (response.status_code if response else "None"))
            return

        self._save_page(response)
        content = response.text
        if content and self._exec_cbk:
            self._exec_cbk(self._parse_html(content), self.depth + 1)

    # 进行HTTP请求，带重试，成功返回Response
    def _make_request(self, retry):
        if retry <= 0 or not strtools.is_http_url(self.url):
            Logger.log("[SpiderJob] arguments illegal. retry=%s, url=%s." % retry, self.url)
            return None

        count = 0
        response = None
        while count < retry and not response:
            count += 1
            try:
                response = requests.get(self.url, timeout=self._timeout, headers=MiniSpiderJob.headers)
            except Exception as e:
                logger.Logger.log("[SpiderJob] request retry %s. Failed for %s", count, e.message)
                pass
        return response

    # 解析网页，或许所有<a>标签中的链接地址
    def _parse_html(self, content):
        links = []
        soup = BeautifulSoup(content, "html.parser")

        slices = urlparse.urlsplit(self.url)
        base = urlparse.urljoin(slices[0], slices[1])

        for a in soup.find_all("a"):
            link = strtools.convert_to_abs_url(base, a.get("href"))
            if strtools.is_http_url(link):
                links.append(link)
        return links

    # 保存网页数据到指定目录位置
    def _save_page(self, resp):
        name = strtools.url_to_filename(self.url)
        file_path = filetools.get_file_path(self._save_dir, name, True)
        f = None
        try:
            f = open(file_path, "w")
            f.write(resp.content)
        except Exception as e:
            print e.message
        finally:
            if f:
                f.close()


def test():
    def cbk(links):
        for l in links:
            print l

    print 'test'
    url = 'http://www.jd.com'
    job = MiniSpiderJob(url, 10, 0, cbk)
    job.execute()
