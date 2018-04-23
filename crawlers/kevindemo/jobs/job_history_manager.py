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

import gevent
from gevent import monkey
from gevent.pool import Pool
from threading import current_thread
import threading
from utils import strtools, filetools
from gevent.queue import Queue
from config import mini_spider_config
from mini_spider_job import MiniSpiderJob

monkey.patch_all()


class JobHistoryManager:
    BATCH_LIMIT = 100
    HISTORY_FILE_NAME = "history.txt"
    _pattern = None
    _history_file = None
    _job_continue = False
    simple_memcache = None
    batch_buf = None

    def __init__(self, spider_config):
        self._pattern = spider_config.target_url
        self._history_file = filetools.get_file_path(spider_config.log_directory, JobHistoryManager.HISTORY_FILE_NAME,
                                                     True)
        self._job_continue = spider_config.job_continue
        self._batch_buf = set()
        self._simple_memcache = set()

        if self._job_continue:
            self._recovery_status()
        else:
            filetools.remove_file(self._history_file)

    # 判断URL是否已经存在任务历史中
    def in_history(self, url):
        if url in self._batch_buf or url in self._simple_memcache:
            return True
        self._batch_buf.add(url)

        if len(self._batch_buf) > JobHistoryManager.BATCH_LIMIT:
            self._flush_data()
        return False

    # 程序异常终止时，保存所有历史数据到文件中
    def save_status(self):
        try:
            self._flush_data()
        except Exception as e:
            print e.message

    # Buffer空间超过LIMIT时，将Buffer中所有URL存入文件
    def _flush_data(self):
        print 'ga'
        f = None
        try:
            f = open(self._history_file, "a+")
            for url in self._batch_buf:
                f.write(url + "\n")
        except Exception as e:
            print "File read failed. %s" % e.message
        finally:
            if f:
                f.close()
        self._simple_memcache.update(self._batch_buf)
        self._batch_buf.clear()

    # 如需继续上次爬虫任务。从历史文件中恢复上次任务进度。
    def _recovery_status(self):
        f = None
        try:
            f = open(self._history_file)
            line = f.readline()
            while line:
                self._simple_memcache.add(line.strip())
                line = f.readline()
        except Exception as e:
            print "File read failed. %s" % e.message
            pass
        finally:
            if f:
                f.close()

    def test(self):
        print self.in_history("a")
        print self.in_history("b")
        print self.in_history("c")
        print self.in_history("d")
        print self.in_history("e")
        print self.in_history("a")
        print self.in_history("b")
        print self.in_history("c")
        print self.in_history("d")
        print self.in_history("e")

        self._simple_memcache.clear()
        self._batch_buf.clear()
        print self._simple_memcache
        self._recovery_status()
        print self._simple_memcache
        self.in_history("d")
        self._flush_data()
        self._simple_memcache.clear()
        self._batch_buf.clear()
        print self._simple_memcache
        self._recovery_status()
        print self._simple_memcache
        self.in_history("time")
        self.in_history("to")
        self.in_history("say goodbye")


def test():
    print 'Test Start'
    m = JobHistoryManager(mini_spider_config.DEFAULT_SPIDER_CONFIG)
    m.test()
    # m2 = JobHistoryManager(mini_spider_config.DEFAULT_SPIDER_CONFIG)
    print 'Test over'
    return m
