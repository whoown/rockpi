#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8') #@UndefinedVariable

from util import Vehicle, Violation, VerifyCode, json_decorator,\
        fetch_http, reg, WrongVerifyCode
import json


headers = {
    'Accept': '*/*',
    'Accept-Charset':'GBK,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'www.gzjd.gov.cn',
    'Origin': 'http://www.gzjd.gov.cn',
    'Referer': 'http://www.gzjd.gov.cn/cgs/html/violation/visitor.html',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'}

captcha_confirm_url = "http://www.gzjd.gov.cn/cgs/captcha/testValidateCaptcha.htm?type=2"
pre_request_url = "http://www.gzjd.gov.cn/cgs/vehiclelicense/checkVisitorVehicle.htm"
request_url = "http://www.gzjd.gov.cn/cgs/violation/getVisitorVioList.htm"
captcha_url = "http://www.gzjd.gov.cn/cgs/captcha/getCaptcha.htm?type=2"

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
    result['name'] = 'guangzhou'
    result['version'] = 1
    
    captcha_data = {"captchaId":verify_code.verify_code}
    count = 0
    while count < 5:
        count += 1
        captcha_resp = fetch_http(captcha_confirm_url, "post", data=captcha_data, headers=verify_code.headers)
        print "captcha_content : ", captcha_resp.content
        if captcha_resp.content.__contains__("fail"):
            print "captcha retry ~!"
            continue
        else:
            break
    else:
        raise WrongVerifyCode()
    
    pre_data = {"hpzl":"02",
                    "hphm":vehicle.license_plate_num,
                    "fdjh":vehicle.engine_num,
                    "clsbdh":vehicle.body_num,
                    "captcha":verify_code.verify_code}
    count = 0
    while count < 5:
        count += 1
        pre_resp = fetch_http(pre_request_url, "post", data=pre_data, headers=verify_code.headers)
        print "pre_content", pre_resp.content
        if pre_resp.content != "":
            break
    if pre_resp.content.__contains__("_error"):
        result['error'] = 'VEHICLE INFO ERROR'
        return result
    key = reg(pre_resp.content, r"(?<=key:)(.+)(?=\$\d+)")[0][0]
    total = reg(pre_resp.content, r"(?<=\$)(\d+)")[0][0]
    if total == "0":
        result['violations'] = []
        return result
    
    data = {"platenumtype":"02",
                    "platenum":vehicle.license_plate_num,
                    "engineno":vehicle.engine_num,
                    "vehicleidnum":vehicle.body_num,
                    "key":key}
    count = 0
    while count < 5:
        count += 1
        main_resp = fetch_http(request_url, "post", data=data, headers=verify_code.headers)
        print "main_content : ", main_resp.content
        if main_resp.content.__contains__('"data":"",'):
            print "retry ~!"
            continue
        else:
            break
    vio_data = json.loads(main_resp.content)
    violations = []
    for elem in vio_data["data"]:
        violation = Violation()
        violation.fine = elem["FKJE"]
        violation.point = elem["WFJFS"]
        violation.address = elem["WFDZ"]
        violation.time = elem["WFSJ"]
        violation.violation_type = elem["WFXWMC"]
        violation.handled = False
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
    vehicle = Vehicle(u'粤AA6D12', u'3136', u'005378')
    result = start_task(vehicle)
