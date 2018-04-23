# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 00:09:47 2018

@author: shenchao05

"""
import re
import urlparse


def is_http_url(url):
    if not url:
        return False
    return True if re.match("^https?://.+$", url) else False


def is_relative_path(url_path):
    if not url_path:
        return False
    return True if re.match("^/.+$", url_path) else False


def convert_to_abs_url(base, url_path):
    if not url_path or is_http_url(url_path):
        return url_path
    if is_relative_path(url_path):
        if url_path.startswith("//"):
            return "http:" + url_path
        elif url_path.startswith("/"):
            return urlparse.urljoin(base, url_path)
    return None


def url_to_filename(url):
    return re.sub("[:?&=/\\\\]", "_", url)


def match_url(reg, url):
    if not reg:
        return True
    if not str:
        return False
    return re.match(reg, url)


if __name__ == '__main__':
    print is_http_url(None)
    print is_http_url("https://www.baidu.com")
    url_to_filename('')
