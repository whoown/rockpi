import requests
from bs4 import BeautifulSoup
import json
import types
import math
import urllib

COMMON_TEST_KEY = "AIzaSyA74jVIJWRSA_M-r-xs9Ah0P0UZrZ5t-ug"

s = requests.Session()
s.headers.update({'Authorization': COMMON_TEST_KEY,
    'Host': 'www.amazon.com',
    'Content-Type': 'application/json'})

def parse_amazon_goods_list(arg_rh, arg_keyword, arg_page):
    ajax_url = amazon_ajax_url + 'ref=sr_pg_'+str(arg_page)
    payloads = {'rh':arg_rh, 'keywords':arg_keyword, 'page':arg_page, 'ie':'UTF8', 'section':'ATF,BTF', 'fromApp':'gp/search', 'fromPage':'results', 'version':'2'}
    ret = s.get(ajax_url, params = payloads)
    
    '''fout = open("C:\Users\Rock\Desktop\d.txt", "w")
    fout.write(ret.text)
    fout.close()'''
    
    # amazon ajax url return multiple json data at one time. separate each others by &&&  
    ajax_datas = ret.text.split('&&&')
    url_goods = []
    
    for data in ajax_datas:
        try:
            jsn = json.loads(data)
        except ValueError:
            continue
        
        html_code = ''
        if jsn.get('center'):
            html_code = jsn['center']['data']['value']
        elif jsn.get('centerBelow'):
            html_code = jsn['centerBelow']['data']['value']
        elif jsn.get('ajaxData'):
            html_code = jsn['ajaxData']['data']['value']
        
        if html_code:
            soup = BeautifulSoup(html_code)
            for goods in soup.find_all("h3"):
                url_goods.append(goods.a['href'])
    
    return url_goods   


def test():
    rh = 'n:1055398,k:Buddhism'
    keyword = 'Buddhism'
    page = 2
    goods = parse_amazon_goods_list(rh, keyword, page)
    for url in goods:
        print url


if __name__ == '__main__':
    map_res = test()
    
    
    
    
    
    