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
    'Host': 'bespeak.zzjtgl.cn',
    'Origin': 'http://bespeak.zzjtgl.cn',
    'Referer': 'http://bespeak.zzjtgl.cn/zxywbl/jdc_cx.aspx?ywdm=A_1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.110 Safari/537.36',
    }

pre_request_url = "http://bespeak.zzjtgl.cn/zxywbl/jdc_cx.aspx?ywdm=A_1"
request_url = "http://bespeak.zzjtgl.cn/zxywbl/jdc_cx.aspx?ywdm=A_1"
captcha_url = "http://bespeak.zzjtgl.cn/zxywbl/GetYzmCode.aspx"

view_state = ""

def get_verify_code(vehicle):
    global view_state
    # first request to get cookie and view_state
    first_resp = fetch_http(pre_request_url, "get")
    view_state = reg(first_resp.content, r'<input.+?id="__VIEWSTATE".+?value="(.+?)"')[0][0]
    print view_state
    verify_resp = fetch_http(captcha_url, 'get', headers=headers)
    headers["Cookie"] = verify_resp.headers['set-cookie']
    print headers
    verify_code = VerifyCode(verify_resp.raw, headers=headers)

    verify_code.recognize()

    return verify_code

@json_decorator
def crawl(vehicle, verify_code=None):
    global view_state
    # do some request with verify_code
    # if verify code is wrong, raise WrongVerifyCode
    # raise WrongVerifyCode()
    
    if verify_code.verify_code == None:
        raise WrongVerifyCode()
    
    result = dict()
    result['name'] = 'zhengzhou'
    result['version'] = 1
    
    data = {"__VIEWSTATE":view_state,
                "txtHphm":vehicle.license_plate_num,
                "txtClsbdh":vehicle.body_num,
                "ddlHpzl":"02",
                "txtYzm":verify_code.verify_code,
                "Button1":" 查　询 "}
    second_resp = fetch_http(request_url, "post", data=data, headers=verify_code.headers)
#    print second_resp.content
    if second_resp.content.__contains__(u"验证码填写有误"):
        raise WrongVerifyCode()
    if second_resp.content.__contains__(u"恭喜您，没有您的违法信息") or second_resp.content.__contains__(u"没有找到相关的车辆信息"):
        result['violations'] = []
        return result
    tr_list = reg(second_resp.content, r"<tr>(<td align='center'>\d{4}-\d{2}-\d{2}.+?)</tr>")
    violations = []
    for tr in tr_list:
        violation = Violation()
        td_infos = reg(tr[0], r"<td.*?>(.+?)</td>")
        violation.fine = td_infos[4][0].strip()
        violation.address = td_infos[1][0].strip()
        violation.time = td_infos[0][0].strip()
        violation.violation_type = td_infos[2][0].strip()
        violation.handled = True
        if td_infos[5][0].strip() == "未交款":
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
    vehicle = Vehicle(u'豫A888XJ', u'', u'LBEJMBJB2BX277731')
    result = start_task(vehicle)
