# coding=utf-8
# -*- coding: UTF-8 -*-
__author__ = 'Rock'
import os
import re
import shutil


def iterate(path, file_callback=None, dir_callback=None):
    if not os.path.exists(path):
        return
    path = os.path.abspath(path)
    if os.path.isfile(path) and callable(file_callback):
        file_callback(path)
    elif os.path.isdir(path):
        if callable(dir_callback):
            dir_callback(path)
        for f in os.listdir(path):
            iterate(os.path.join(path, f), file_callback, dir_callback)


if __name__ == '__main__':
    path = '/Users/zhangyan/Work/git/buding/Hulk'
    def pf(path):
        print path
    func = pf
    def pd(path):
        print "### "+path
    f2 = pd
    iterate(path, func, f2)
