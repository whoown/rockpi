# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 00:09:47 2018

@author: shenchao05

"""


class Logger():

    @staticmethod
    def log(*args, **kwargs):
        print(args, kwargs)


if __name__ == '__main__':
    Logger.log(12, 'time', 232, jk='time', fuck='time')
