#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8') #@UndefinedVariable

from util import Vehicle, Violation, json_decorator, fetch_http, reg
import traceback

headers = {
    'Accept': '*/*',
    'Accept-Charset':'GBK,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Host': 'jx.jxhld.gov.cn:8088',
    'Origin': 'http://jx.jxhld.gov.cn:8088',
    'Referer': 'http://jx.jxhld.gov.cn:8088/zhcx/web/car_jsp/car_wf.jsp',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.110 Safari/537.36'}

pre_request_url = "http://jx.jxhld.gov.cn:8088/zhcx/web/car_jsp/car_wf.jsp"
post_url = 'http://jx.jxhld.gov.cn:8088/car/cc.do'

proxies = {
    #'http' : '127.0.0.1:8087'
    #'http' : '107.0.69.189:3128'
}
@json_decorator
def crawl(vehicle):
    result = dict()
    result['name'] = 'jiangxi'
    result['version'] = 1

    car_type = "02"
    car_no = vehicle.license_plate_num.encode("utf-8")
    body_no = vehicle.body_num
    data = {"a": car_type,
            "b": car_no,
            "c": body_no,
            "x": car_type,
            "y": car_no,
            "z": body_no,
            "w": car_type,
            "e": car_no,
            "s": body_no,
            "v": car_type,
            "x": car_no,
            "q": body_no,
            "j": car_type,
            "k": car_no,
            "l": body_no+"3a="+car_type,
            "b4": car_no,
            "c="+body_no+"4a": car_type,
            "gb": car_no,
            "gz": car_no,
            "cc": body_no+"2a="+car_type,
            "cb": car_no,
            "c1": body_no+"vb="+car_type,
            "av": car_no,
            "ab": body_no,
            "pageRecords":"100",
            "currPage":"1"}

    pre_response = fetch_http(url=pre_request_url, method='get', proxies=proxies)
    g = reg(pre_response.content, r"g\s+=\s*'(\w+)'")
    headers["Cookie"] = pre_response.headers['Set-Cookie']
    data["g"] = g[0][0]

    values = ""
    for key in data:
        values += key+"="+data[key]+"&"
    
    headers['X-Requested-With'] = 'XMLHttpRequest'
    for i in range(5):
        base_response = fetch_http(
                url=post_url,
                method='post',
                data=values[:-1],
                headers=headers,
                proxies=proxies)
        print base_response.content
        if u"该信息不存在" in base_response.content or\
                u"查询超时" in base_response.content:
            continue
        else:
            break
    else:
        result['error'] = 'NET ERROR'
        return result

    content = base_response.content

    if u'很抱歉，您的计算机已超过今天最大查询次数，请明天再使用' in content:
        result['error'] = 'NET ERROR'
        return result

    if u'您输入车牌号码或机动车类型不正确' in content or\
            u'您输入车架号后6位不正确' in content:
        # vehicle info error
        result['error'] = 'VEHICLE INFO ERROR'
        return result
    if u'该车辆暂无违法信息' in content:
        # vehicle has no violation
        result['violations'] = []
        return result
    
    time_reg_result = reg(content, r"\d{4}-\d{2}-\d{2}\s{1}\d{2}:\d{2}")
    time_dict = {}
    for time_str in time_reg_result:
        if time_str[0] in time_dict:
            time_dict[time_str[0]] += 1
        else:
            time_dict[time_str[0]] = 1
    time_list = []
    for key in time_dict:
        if time_dict[key] == 1:
            time_list.append(key)
    time_list.sort(reverse=True)
    
    address_reg_result = reg(
            content,
            r"' style=\"padding-left:5px\" align='left'>(.+?)</td>")
    
    code_reg_result = reg(
            content,
            r"<span title=''>(.+?)</span>")
    
    agency_reg_result = reg(
            content,
            r'style="padding-left:5px" align="left">(.+?)</td>')
    
    violations = []
    for i in range(len(time_list)):
        violation = Violation()
        violation.time = time_list[i]
        violation.violation_type = code_reg_result[i][0]
        violation.address = address_reg_result[i][0]
        violation.agency = agency_reg_result[i][0]
        violation.handled = False
        violations.append(dict(violation))

    result['violations'] = violations
    return result

if __name__ == '__main__':
    vehicle = Vehicle(u'赣AE2728', u'', u'203074')
    print crawl(vehicle)
