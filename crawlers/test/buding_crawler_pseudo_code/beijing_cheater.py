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
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
    'Connection':'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'sslk.bjjtgl.gov.cn',
    'Origin': 'http://sslk.bjjtgl.gov.cn',
    'Referer': 'http://www.bjjtgl.gov.cn/portals/0/weifachaxun/newsy_wfchaxun.htm',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.110 Safari/537.36',
    }

pre_referer_for_beijing = "http://www.bjjtgl.gov.cn/portals/0/weifachaxun/newsy_wfchaxun.htm"
pre_referer_for_other = "http://sslk.bjjtgl.gov.cn/jgjwwcx/wzcx/wzcx_preview.jsp"
referer = "http://sslk.bjjtgl.gov.cn/jgjwwcx/wzcx/wzcx_preview.jsp"

pre_request_url = "http://www.bjjtgl.gov.cn/publish/portal0/"
mid_request_url_for_beijing = "http://sslk.bjjtgl.gov.cn/jgjwwcx/wzcx/wzcx_preview.jsp"
mid_request_url_for_other = "http://sslk.bjjtgl.gov.cn/jgjwwcx/wzcx/getHpzlList4MoblieYzm.action"
request_url = "http://sslk.bjjtgl.gov.cn/jgjwwcx/wzcx/getWzcxXx.action"

captcha_url = "http://sslk.bjjtgl.gov.cn/jgjwwcx/servlet/YzmImg"

sf_dic = {"京":11,"津":12,"冀":13,"晋":14,"蒙":15,"辽":21,"吉":22,"黑":23,"沪":31,"苏":32,"浙":33,"皖":34,"闽":35,"赣":36,"鲁":37,"豫":41,"鄂":42,"湘":43,"粤":44,"桂":45,"琼":46,"渝":50,"川":51,"贵":52,"云":53,"藏":54,"陕":61,"甘":62,"青":63,"宁":64,"新":65,"台":71}

cxlm = ""
sf = 11

def first_request():
    global cxlm, chfs, sf
    # first request to get cookie
    if unicode(vehicle.license_plate_num)[0].encode("utf-8") in sf_dic:
        sf = sf_dic.get(unicode(vehicle.license_plate_num)[0].encode("utf-8"))
    
    if sf == 11:
        pre_data = {"sf":sf,
                            "carno":vehicle.license_plate_num[-6:],
                            "fdjh":vehicle.engine_num}
        headers["Referer"] = pre_referer_for_beijing
        first_resp = fetch_http(mid_request_url_for_beijing, "post", data=pre_data, headers=headers)
    else:
        vehicle.engine_num = "wd"
        pre_data = {"sf":sf,
                            "carnono":vehicle.license_plate_num[-6:],
                            "fdjhhm":vehicle.engine_num}
        headers["Referer"] = pre_referer_for_other
        first_resp = fetch_http(mid_request_url_for_other, "post", data=pre_data, headers=headers)
    headers["Cookie"] = first_resp.headers['set-cookie']
    cxlm = reg(first_resp.content, r'id="cxlm" value="(.*?)"')[0][0]

def get_verify_code(vehicle):
    # return None for none verify code
    print headers
    verify_resp = fetch_http(captcha_url, 'get', headers=headers)
    verify_code = VerifyCode(verify_resp.raw, headers=headers)

    verify_code.recognize()

    return verify_code

@json_decorator
def crawl(vehicle, verify_code=None):
    global cxlm, chfs, sf
    # do some request with verify_code
    # if verify code is wrong, raise WrongVerifyCode
    # raise WrongVerifyCode()
    
    if verify_code.verify_code == None:
        raise WrongVerifyCode()
    
    result = dict()
    result['name'] = 'beijing_new'
    result['version'] = 1
    
    data = {"sf":sf,
                "fdjhhm":vehicle.engine_num.encode("utf-8"),
                "carnono":vehicle.license_plate_num[-6:],
                "cxlm":cxlm,
                "yzm":verify_code.verify_code}
    if sf == 11:
        data["chfs"] = ""
    else:
        data["hpzllb"] = "02"
    print data
    second_resp = fetch_http(request_url, "post", data=data, headers=verify_code.headers)

    if second_resp.content.__contains__(u"验证码输入有误"):
        raise WrongVerifyCode()
    if second_resp.content.__contains__(u"您输入的车牌号或发动机号有误") or second_resp.content.__contains__(u"您没有输入完整的车牌号和发动机号"):
        result['error'] = 'VEHICLE INFO ERROR'
        return result
    if second_resp.content.__contains__(u"您没有未接受处理的违法记录") or second_resp.content.__contains__(u"您没有未接受处理的在京违法记录"):
        result['violations'] = []
        return result
    
    tr_list = reg(second_resp.content, r"<tr[\s\S]+?(<td>\d{4}-\d{2}-\d{2}[\s\S]+?)</tr>")
    violations = []
    for tr in tr_list:
        violation = Violation()
        tds = reg(tr[0], r"<td.*?>([\s\S]+?)</td>")
        violation.fine = tds[4][0]
        violation.address = tds[1][0]
        violation.time = tds[0][0]
        violation.violation_type = reg(tds[2][0], r"<a.+?>(.+?)</a>")[0][0]
        handled = True
        if tds[5][0].encode("utf-8") == "未处理":
            handled = False
        violation.handled = handled
        violation.point = tds[3][0]
        violation.agency = ""
        violations.append(dict(violation))
        
        print violation.time
        print violation.address
        print violation.violation_type
        print violation.fine
        print violation.point
        print violation.handled
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
#    vehicle = Vehicle(u'京N56N98', u'559036B', u'')
    vehicle = Vehicle(u'冀F270A8', u'', u'')
    result = start_task(vehicle)
