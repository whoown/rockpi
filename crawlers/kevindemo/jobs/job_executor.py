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
from gevent.queue import Queue
from config import mini_spider_config

from job_history_manager import JobHistoryManager
from mini_spider_job import MiniSpiderJob
from utils import strtools, filetools

monkey.patch_all()


class MiniSpiderJobExecutor:
    _log_dir = None
    _output_dir = None
    _executing = False
    _config = None
    _pool = None
    _pool_snapshot = None
    _job_queue = Queue()
    _history_manager = None

    def __init__(self, spider_config):
        self._config = spider_config if spider_config else mini_spider_config.DEFAULT_SPIDER_CONFIG
        self._log_dir = self._config.log_directory
        self._output_dir = self._config.output_directory

    # 开始运行所有爬虫任务。此函数的调用线程/协程将进入等待状态，直到所有任务完成或爬虫运行超时。
    def execute(self):
        if self._executing:
            return
        self._executing = True
        self._pool = Pool(self._config.thread_count)
        self._history_manager = JobHistoryManager(self._config)

        # 继续上次任务，不再重新启动
        if self._config.job_continue:
            self._recovery_status()
        else:
            # 清理环境后，重新加载种子文件
            self._clean_context()
            seeds = self._config.get_url_list()
            for seed in seeds:
                new_job = MiniSpiderJob(seed, self._output_dir, self._config.crawl_timeout, 0,
                                        self._executor_callback)
                self._job_queue.put_nowait(new_job)

        self._pool_snapshot = []
        for coroutine_id in range(self._pool.size):
            self._pool_snapshot.append(None)
            self._pool.spawn(self._coroutine_execute, coroutine_id)
        gevent.joinall(self._pool, self._config.spider_timeout)
        self._executing = False

    # 协程池协程任务。
    def _coroutine_execute(self, cor_id):
        print 'Coroutine Id is %s' % cor_id
        while not self._all_jobs_completed():
            job = self._job_queue.get(block=True)
            print 'Coroutine%s get job %s ' % (cor_id, job)
            self._pool_snapshot[cor_id] = job
            job.execute()
            self._pool_snapshot[cor_id] = None
            gevent.sleep(self._config.crawl_interval)
        self._pool.kill()
        print 'Coroutine%s exit: ' % cor_id

    # 任一爬虫Job（某个URL）工作完毕后的回调。
    def _executor_callback(self, sub_urls, depth):
        if depth > self._config.max_depth:
            print 'Reach the max depth. Ignore all sub urls'
            return

        reg = self._config.target_url
        for u in sub_urls:
            if not strtools.match_url(reg, u):
                continue
            if self._history_manager.in_history(u):
                continue
            job = MiniSpiderJob(u, self._output_dir, self._config.crawl_timeout, depth, self._executor_callback)
            print '-----new job', u
            self._job_queue.put_nowait(job)

    # 判断是否所有爬虫任务全部完成。满足：1.无正在执行的任务；2.队列中无等待任务
    def _all_jobs_completed(self):
        no_job_executing = True
        for snap in self._pool_snapshot:
            if snap:
                no_job_executing = False
        return no_job_executing and self._job_queue.empty()

    # 程序异常退出时，保存现场
    def save_status(self):
        self._history_manager.save_status()
        file_path = filetools.get_file_path(self._log_dir, "exec_status.txt", True)
        f = None
        try:
            f = open(file_path, "w")
            for job in self._job_queue:
                f.write("%s %s\n" % (job.url, job.depth))
        except Exception as e:
            print e.message
        finally:
            if f:
                f.close()

    # 程序异常退出后再次启动时，根据配置要求，恢复现场
    def _recovery_status(self):
        file_path = filetools.get_file_path(self._log_dir, "exec_status.txt", True)
        f = None
        try:
            f = open(file_path, "r")
            line = f.readline()
            while line:
                jobstat = line.split()
                job = MiniSpiderJob(jobstat[0], self._output_dir, self._config.crawl_timeout, jobstat[1],
                                    self._executor_callback)
                self._job_queue.put_nowait(job)
                line = f.readline()
        except Exception as e:
            print e.message
        finally:
            if f:
                f.close()

    # 开始运行爬虫程序前，清理环境
    def _clean_context(self):
        filetools.remove_file(self._log_dir)
        filetools.remove_file(self._output_dir)


def test():
    print 'Test Start'
    executor = MiniSpiderJobExecutor(None)
    executor.execute()
    print 'Test over'
    pass
