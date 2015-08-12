#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8') #@UndefinedVariable

from util import Vehicle, Violation, VerifyCode, json_decorator,\
        fetch_http, reg, WrongVerifyCode


headers = {
    'Accept': '*/*',
    'Accept-Charset':'GBK,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'www.gddgcgs.gov.cn',
    'Origin': 'http://www.gddgcgs.gov.cn',
    'Referer': 'http://www.gddgcgs.gov.cn/Illegal.aspx',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'}

pre_request_url = "http://www.gddgcgs.gov.cn/Illegal.aspx"
request_url = "http://www.gddgcgs.gov.cn/Ajax.aspx"
captcha_url = "http://www.gddgcgs.gov.cn/CheckCode.aspx"

gg_value = ""

def first_request():
    global gg_value
    # first request to get cookie
    first_resp = fetch_http(pre_request_url, "get")
    headers["Cookie"] = first_resp.headers['set-cookie']
    gg_value = reg(first_resp.content, r"this,'(\w+?)'")[0][0]

def get_verify_code(vehicle):
    # return None for none verify code
    verify_resp = fetch_http(captcha_url, 'get', headers=headers)
    verify_code = VerifyCode(verify_resp.raw, headers=headers)

    verify_code.recognize()

    return verify_code

@json_decorator
def crawl(vehicle, verify_code=None):
    global gg_value
    # do some request with verify_code
    # if verify code is wrong, raise WrongVerifyCode
    # raise WrongVerifyCode()
    
    if verify_code.verify_code == None:
        raise WrongVerifyCode()
    
    result = dict()
    result['name'] = 'dongguan'
    result['version'] = 1
    
    data = {"action":"Illagel",
                "headno":vehicle.license_plate_num[:-6],
                "no":vehicle.license_plate_num[-6:],
                "back4":vehicle.body_num,
                "fdjh6":vehicle.engine_num,
                "validate":verify_code.verify_code,
                "type":"02",
                "tele":"18607325868",
                "gg":gg_value}
    
    for k in data.keys():
        print k, data[k] 
    
    
    second_resp = fetch_http(request_url, "post", data=data, headers=verify_code.headers)

    if second_resp.content.__contains__(u"验证码错误"):
        raise WrongVerifyCode()
    if second_resp.content.__contains__(u"发动机号错误") or second_resp.content.__contains__(u"车架号错误") or second_resp.content.__contains__(u"车辆信息错误"):
        result['error'] = 'VEHICLE INFO ERROR'
        return result
    if second_resp.content.__contains__(u"没有违章信息"):
        result['violations'] = []
        return result
    
    tr_list = reg(second_resp.content, r"<tr><td>(.+?</table></td>.+?)</td></tr>")
    violations = []
    for tr in tr_list:
        violation = Violation()
        violation.fine = reg(tr[0], r"<td>(\d{1,6}?)</td><td>")[0][0]
        sub_table_content = reg(tr[0], r'<table class="illegal_table".+?>(.+?)</table>')[0][0]
        sub_info_list = reg(sub_table_content, r'<td[^r]*?>(.+?)</td>')
        violation.address = sub_info_list[2][0]
        violation.time = sub_info_list[0][0].replace("年","-").replace("月","-").replace("日","").replace("时",":").replace("分",":").replace("秒","")
        violation.violation_type = sub_info_list[3][0]
        violation.handled = False
        point = sub_info_list[1][0][1]
        if point == "7":
            point = "12"
        violation.point = point
        violation.agency = ""
        violations.append(dict(violation))
    result['violations'] = violations
    return result

def start_task(vehicle):
    first_request()
    verify_info = get_verify_code(vehicle)
    result = crawl(vehicle, verify_info)
    print result

if __name__ == '__main__':
#    get_verify_code("")
    vehicle = Vehicle(u'粤SDP868', u'883782', u'519134')
    result = start_task(vehicle)
