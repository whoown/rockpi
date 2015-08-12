#!/usr/bin/python
# -*- coding: utf-8 -*-

from functools import wraps
import json
import re

import requests

class Vehicle(object):
    def __init__(self, license_plate_num=None, engine_num=None, body_num=None):
        self.license_plate_num = license_plate_num.upper()
        self.engine_num = engine_num.upper()
        self.body_num = body_num.upper()


class Violation(object):
    def __init__(self, time=None, violation_type=None, address=None,
            fine=0, point=0, handled=False, agency=None):
        self.time = time
        self.violation_type = violation_type
        self.address = address
        self.fine = fine
        self.point = point
        self.handled = handled
        self.agency = agency

    def __iter__(self):
        l = [
                ('time', self.time),
                ('violation_type', self.violation_type),
                ('address', self.address),
                ('fine', self.fine),
                ('point', self.point),
                ('handled', self.handled),
                ('agency', self.agency)]
        return l.__iter__()


class HttpResponse(object):
    def __init__(self, content=None, status_code=None, headers=None, raw=None):
        self.content = content
        self.status_code = status_code
        self.headers = headers
        self.raw = raw


class VerifyCode(object):
    def __init__(self, raw=None, verify_code=None, headers=None):
        self.raw = raw
        self.verify_code = verify_code
        self.headers = headers

    def recognize(self):
        f = open('C:\\Users\\Rock\\Desktop\\test.png', 'wb')
        f.write(self.raw)
        f.flush()
        f.close()
#        print self.raw

        self.verify_code = raw_input('input the verify code: ')


class WrongVerifyCode(Exception):
    pass


def fetch_http(url, method, data={}, headers={}, proxies={}):
    if method == 'get':
        ret = requests.get(url, headers=headers, proxies=proxies)
    else:
        ret = requests.post(url, headers=headers, data=data, proxies=proxies)
    return HttpResponse(ret.text, ret.status_code, ret.headers, ret.content)

def reg(content, r):
    match_list = re.findall(r, content)
    result_list = []
    for m in match_list:
        if isinstance(m, tuple):
            result_list.append(list(m))
        else:
            result_list.append([m])
    return result_list

def json_decorator(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        ret = f(*args, **kwargs)
        return json.dumps(ret)
    return decorator
