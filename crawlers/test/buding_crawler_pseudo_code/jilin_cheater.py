#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8') #@UndefinedVariable

from util import Vehicle, Violation, VerifyCode, json_decorator,\
        fetch_http, reg, WrongVerifyCode


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset':'GBK,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'www.jljj.cn',
    'Origin': 'http://www.jljj.cn',
    'Referer': 'http://www.jljj.cn/',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.110 Safari/537.36',
    }

request_url = "http://www.jljj.cn/thirdparty/cx/cgcx.jsp"
captcha_url = "http://www.jljj.cn/thirdparty/cx/val.jsp"

def get_verify_code(vehicle):
    # return None for none verify code
    verify_resp = fetch_http(captcha_url, 'get', headers=headers)
    headers["Cookie"] = verify_resp.headers['set-cookie']
    print headers
    verify_code = VerifyCode(verify_resp.raw, headers=headers)

    verify_code.recognize()

    return verify_code

@json_decorator
def crawl(vehicle, verify_code=None):
    # do some request with verify_code
    # if verify code is wrong, raise WrongVerifyCode
    # raise WrongVerifyCode()
    
    if verify_code.verify_code == None:
        raise WrongVerifyCode()
    
    result = dict()
    result['name'] = 'jilin'
    result['version'] = 1
    
    data = {"province":vehicle.license_plate_num[:-6],
                "hphm":vehicle.license_plate_num[-6:],
                "engine":vehicle.body_num[-4:],
                "yzm":verify_code.verify_code.strip(),
                "hpzl":"02"}
    second_resp = fetch_http(request_url, "post", data=data, headers=verify_code.headers)
#    print second_resp.content
#    return
    if second_resp.content.__contains__(u"验证码错误"):
        raise WrongVerifyCode()
    if second_resp.content.__contains__(u"车辆识别代号后四位输入有误"):
        result['error'] = 'VEHICLE INFO ERROR'
        return result
    
    result_table = reg(second_resp.content, r'<table id="wzjl_table"[\s\S]+?>([\s\S]+?)</table>')
    tr_list = reg(result_table[0][0], r"<tr>([\s\S]+?)</tr>")
    violations = []
    for tr in tr_list:
        violation = Violation()
        tds = reg(tr[0], r"<td[\s\S]+?>([\s\S]+?)</td>")
        violation.fine = tds[4][0].strip()
        violation.address = tds[3][0].strip()
        violation.time = tds[2][0].strip()
        violation.violation_type = tds[6][0].strip()
        violation.handled = False
        violation.point = tds[5][0].strip()
        violation.agency = ""
        violations.append(dict(violation))
    result['violations'] = violations
    return result

def start_task(vehicle):
    verify_info = get_verify_code(vehicle)
    result = crawl(vehicle, verify_info)
    print result

if __name__ == '__main__':
#    get_verify_code("")
    vehicle = Vehicle(u'吉AX5716', u'', u'0986')
    result = start_task(vehicle)
