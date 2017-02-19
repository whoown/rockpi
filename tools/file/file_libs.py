# coding=utf-8
# -*- coding: UTF-8 -*-
__author__ = 'Rock'
import os
import re

__ILLEGAL_FILENAME_CHARS = re.compile('[\\\\/:*?"<>|]')


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


def correct_file_name(filename, replace_char='_'):
    return __ILLEGAL_FILENAME_CHARS.sub(replace_char, filename)


def make_sure_dir(dir_path):
    if os.path.isdir(dir_path):
        return True
    else:
        try:
            os.makedirs(dir_path)
        except:
            pass
        return os.path.isdir(dir_path)


def fix_media_file_name(file_path):
    if not os.path.isfile(file_path):
        return
    file_name = os.path.basename(file_path)
    file_name = re.sub("\(\d\)", "", file_name)
    new_path = os.path.join(os.path.dirname(file_path), file_name)
    print new_path
    os.rename(file_path, new_path)


if __name__ == '__main__':
    def cbk(path):
        fix_media_file_name(path)

    path = "/Users/zhangyan/Records"
    iterate(path, cbk)
