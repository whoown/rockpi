#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8') #@UndefinedVariable

from util import Vehicle, Violation, VerifyCode, json_decorator,\
        fetch_http, reg, WrongVerifyCode


def get_verify_code(vehicle):
    # return None for none verify code
    verify_code_img = fetch_http('http://docs.python-requests.org/en/latest/_static/requests-sidebar.png', 'get')
    verify_code = VerifyCode(verify_code_img.raw, '')

    verify_code.recognize()

    return verify_code

@json_decorator
def crawl(vehicle, verify_code=None):
    # do some request with verify_code
    # if verify code is wrong, raise WrongVerifyCode
    # raise WrongVerifyCode()

    # right verify code
    result = dict()
    return result

def start_task(vehicle):
    while True:
        try:
            verify_code = get_verify_code(vehicle)
            return crawl(vehicle, verify_code)
        except WrongVerifyCode, e:
            pass

if __name__ == '__main__':
    start_task(None)
