#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from util import Vehicle, Violation, json_decorator, fetch_http, reg

sf_dic = {
        u'京': 11, u'津': 12, u'冀': 13, u'晋': 14, u'蒙': 15, u'辽': 21,
        u'吉': 22, u'黑': 23, u'沪': 31, u'苏': 32, u'浙': 33, u'皖': 34,
        u'闽': 35, u'赣': 36, u'鲁': 37, u'豫': 41, u'鄂': 42, u'湘': 43,
        u'粤': 44, u'桂': 45, u'琼': 46, u'渝': 50, u'川': 51, u'贵': 52,
        u'云': 53, u'藏': 54, u'陕': 61, u'甘': 62, u'青': 63, u'宁': 64,
        u'新': 65, u'台': 71}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'max-age=0', # optional
    'Connection': 'keep-alive', # optional
    'Content-Length': '61', # optional
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'sslk.bjjtgl.gov.cn',
    'Origin': 'http://sslk.bjjtgl.gov.cn',
    'Referer': 'http://sslk.bjjtgl.gov.cn/jgjww/wzcx/wzcx_yzm.jsp?flag=1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.110 Safari/537.36'}

post_url = 'http://sslk.bjjtgl.gov.cn/jgjww/wzcx/wzcx_result.jsp'
vio_info_base_url = 'http://sslk.bjjtgl.gov.cn/jgjww/wzcx/'

@json_decorator
def crawl(vehicle):
    result = dict()
    result['name'] = 'beijing'
    result['version'] = 1

    sf = sf_dic.get(vehicle.license_plate_num[0], '')
    if not sf:
        result['error'] = 'VEHICLE INFO ERROR'
        return result

    data = {
            'sf': sf,
            'fdjh': vehicle.engine_num,
            'hpzl': '02',
            'hphm': vehicle.license_plate_num[-6:],
            'carno': ''}

    base_response = fetch_http(
            url=post_url,
            method='post',
            data=data,
            headers=headers)
    if u'您没有输入完整的车牌号和发动机号' in base_response.content:
        # vehicle info error
        result['error'] = 'VEHICLE INFO ERROR'
        return result
    if u'您没有未接受处理的违法记录' in base_response.content:
        # vehicle has no violation
        result['violations'] = []
        return result

    base_reg_result = reg(
            base_response.content,
            r'<tr onMouseOver="this.style.backgroundColor=\'ff9900\'"([\s\S]*?)</tr>')

    violations = []
    for v in base_reg_result:
        violation = Violation()

        vio_reg_results = reg(v[0], r'<td.*?>([\s\S]*?)</td>')

        # violation time, address, handled
        violation.time = vio_reg_results[1][0]
        violation.address = vio_reg_results[2][0]
        if vio_reg_results[4][0] == u'未处理':
            violation.handled = False
        else:
            violation.handled = True

        # violation violation_type, fine and point
        reg(vio_reg_results[3][0], r'wzdm=([\s\S]*?)\'')[0][0]
        violation.fine = 0
        violation.point = 0
        violation.violation_type = reg(
                vio_reg_results[3][0],
                r'wzdm=([\s\S]*?)\'')[0][0]

        violations.append(dict(violation))

    result['violations'] = violations
    return result

if __name__ == '__main__':
    vehicle = Vehicle(u'京P50325', u'651095A', u'')
    print crawl(vehicle)
