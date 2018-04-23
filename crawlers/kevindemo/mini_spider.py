# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 00:09:47 2018

@author: shenchao05

"""

import getopt, sys

import utils.logger
from config.mini_spider_config import MiniSpiderConfig
from jobs.job_executor import MiniSpiderJobExecutor
from jobs import mini_spider_job, job_executor, job_history_manager
import atexit


def exit_handler(executor):
    print 'In exit handler'
    executor.save_status()
    pass


def main(argv):
    config_file = None
    try:
        opts, args = getopt.getopt(argv, "hc:", ["config="])
    except getopt.GetoptError:
        print 'mini_spider.py -c <config_file_path>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'mini_spider.py -c <config_file_path> '
            sys.exit()
        elif opt in ("-c", "--config"):
            config_file = arg

    spider_config = MiniSpiderConfig(config_file)
    executor = MiniSpiderJobExecutor(spider_config)
    atexit.register(exit_handler, executor)
    executor.execute()
    print 'Mini Spider Complete all missions!'


if __name__ == '__main__':
    main(sys.argv[1:])
