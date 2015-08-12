#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8') #@UndefinedVariable

from util import Vehicle, Violation, VerifyCode, json_decorator,\
        fetch_http, reg, WrongVerifyCode
import json
import random

proxies = {
    'http' : '115.28.2.165:80'
    #'http' : '107.0.69.189:3128'
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset':'GBK,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'www.ttdaiban.com',
    'Origin': 'http://www.ttdaiban.com',
    'Referer': 'http://www.ttdaiban.com/wzcx.asp',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.110 Safari/537.36',
    }

pre_request_url = "http://www.ttdaiban.com/wzcx.asp"
request_url = "http://www.ttdaiban.com/wzcx.asp?action=renew"
captcha_url = "http://www.ttdaiban.com/getcode.asp"

def first_request():
    # first request to get cookie
    first_resp = fetch_http(pre_request_url, "get", proxies=proxies)
    print first_resp.headers
    headers["Cookie"] = first_resp.headers['set-cookie']

def get_verify_code(vehicle):
    # return None for none verify code
    verify_resp = fetch_http(captcha_url, 'get', headers=headers, proxies=proxies)
    verify_code = VerifyCode(verify_resp.raw, headers=headers)

    verify_code.recognize()

    return verify_code

@json_decorator
def crawl(vehicle, verify_code=None):
    # if verify code is wrong, raise WrongVerifyCode
    # raise WrongVerifyCode()
    
    if verify_code.verify_code == None:
        raise WrongVerifyCode()
    
    result = dict()
    result['name'] = 'guangdong'
    result['version'] = 1
    
    data = {
                "province":vehicle.license_plate_num[:-6].encode("gb2312"),
                "hphm":vehicle.license_plate_num[-6:],
                "CJHM":vehicle.body_num[-6:],
                "fdjh":vehicle.body_num[-6:],
                "mofei":verify_code.verify_code,
                "hpzl":"02",
                "x":random.randint(10, 99),
                "y":random.randint(10, 99)
                }
    
    print data
    
    second_resp = fetch_http(request_url, "post", data=data, headers=verify_code.headers, proxies=proxies)
    print second_resp.content
#    return
    if second_resp.content.__contains__(u"车辆目前无未处理的违章记录"):
        result['violations'] = []
        return result
    if second_resp.content.__contains__(u"您查询的次数过多") or second_resp.content.__contains__(u"系统繁忙，请等待30秒后再查"):
        result['error'] = 'NETWORK ERROR'
        return result
    
    tr_list = reg(second_resp.content, r'<tr.*?>[\s\S]+?(<td.+\d{4}-\d{2}-\d{2} \d{2}:\d{2}[\s\S]+?)</tr>')
    violations = []
    further_request_url_prefix = "http://www.ttdaiban.com/"
    for tr in tr_list:
        tds = reg(tr[0], r'<td.*?>(.*?)</td>')
        further_request_url_suffix = reg(tds[1][0], r"<a.+'../(.+?)'")[0][0]
#        print further_request_url_prefix+further_request_url_suffix
        further_resp = fetch_http(further_request_url_prefix+further_request_url_suffix, "get", headers=verify_code.headers, proxies=proxies)
#        print further_resp.content
        sec_tds = reg(further_resp.content.encode("utf-8"), r"<td.*?>.+?：(.+?)</td>")
        violation = Violation()
        violation.fine = sec_tds[6][0].strip()
        violation.address = reg(sec_tds[3][0], r".*】([\S]+)")[0][0].strip()
        violation.time = sec_tds[2][0].strip()
        violation.violation_type = sec_tds[4][0].strip()
        violation.handled = False
        violation.point = reg(sec_tds[5][0], r"\[.*?(\d+?).*?分\]")[0][0].strip()
        violation.agency = ""
        violations.append(dict(violation))
        
        print violation.time
        print violation.address
        print violation.violation_type
        print violation.fine
        print violation.point
        print " -------- "
    result['violations'] = violations
    return result

def start_task(vehicle):
    first_request()
    verify_info = get_verify_code(vehicle)
    result = crawl(vehicle, verify_info)
    print result

if __name__ == '__main__':
    
#    get_verify_code("")
#    vehicle = Vehicle(u'粤AW8Y46', u'3136', u'198000')
    vehicle = Vehicle(u'粤AA6D12', u'3136', u'005378')
#    vehicle = Vehicle(u'粤AT776A', u'0381', u'152872')
    result = start_task(vehicle)
