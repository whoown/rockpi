# -*- coding: utf-8 -*-
"""
Created on Sun Apr 08 10:55:25 2018

@author: shenchao05
https://www.cnblogs.com/feeland/p/4514771.html
"""

import requests
from bs4 import BeautifulSoup

from inspect import isfunction
import urlparse
import os.path
import ConfigParser


class MiniSpiderConfig:
    url_list_file = None  # 种子文件路径
    output_directory = '.'  # 抓取结果存储目录
    log_directory = '.'  # log日志保存目录
    max_depth = 1  # 最大抓取深度(种子为0级)
    crawl_interval = 1  # 抓取间隔. 单位: 秒
    crawl_timeout = 1  # 抓取超时. 单位: 秒
    spider_timeout = 60 * 60  # 爬虫运行超时。单位：秒
    target_url = None  # .*.(htm|html)$ ; 需要存储的目标网页URL pattern(正则表达式)
    thread_count = 1  # 抓取线程数
    job_continue = False  # 是否继续上一次爬虫任务。默认False，重新开始爬虫任务。
    _url_list = None
    #
    # def __init__(self, url_list_file, output_directory, log_directory, max_depth, crawl_interval, crawl_timeout,
    #              spider_timeout, target_url, thread_count, job_continue):
    #     self.url_list_file = url_list_file
    #     self.output_directory = output_directory
    #     self.log_directory = log_directory
    #     self.max_depth = max_depth
    #     self.crawl_interval = crawl_interval
    #     self.crawl_timeout = crawl_timeout
    #     self.spider_timeout = spider_timeout
    #     self.target_url = target_url
    #     self.thread_count = thread_count
    #     self.job_continue = job_continue

    def __init__(self, config_file):
        if not os.path.isfile(config_file):
            return
        cf = ConfigParser.ConfigParser()
        cf.read(config_file)
        self.url_list_file = cf.get("spider", "url_list_file")
        self.output_directory = cf.get("spider", "output_directory")
        self.log_directory = cf.get("spider", "log_directory")
        self.max_depth = cf.getint("spider", "max_depth")
        self.crawl_interval = cf.getint("spider", "crawl_interval")
        self.spider_timeout = cf.getint("spider", "spider_timeout")
        self.target_url = cf.get("spider", "target_url")
        self.thread_count = cf.getint("spider", "thread_count")
        self.job_continue = cf.getboolean("spider", "job_continue")

    def get_url_list(self):
        if self._url_list:
            return self._url_list
        f = None
        self._url_list = []
        try:
            f = open(self.url_list_file)
            line = f.readline()
            while line:
                self._url_list.append(line.strip())
                line = f.readline()
        except Exception as e:
            print "File read failed. %s" % e.message
            pass
        finally:
            if f:
                f.close()
        return self._url_list


# DEFAULT_SPIDER_CONFIG = MiniSpiderConfig('/Users/zhangyan/Desktop/urls.txt', '/Users/zhangyan/Desktop/output',
#                                          '/Users/zhangyan/Desktop/log', 1, 1,
#                                          10, 60 * 60, ".*.(htm|html)$", 5, False)
