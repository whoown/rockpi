# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 00:09:47 2018

@author: shenchao05

"""
import os.path


def get_file_path(path, filename, makedir):
    f = filename
    if path:
        if not os.path.isdir(path):
            os.mkdir(path)
        f = os.path.join(path, filename)
    return os.path.abspath(f)


def remove_file(filepath):
    try:
        os.remove(filepath)
    except Exception as e:
        print e.message
