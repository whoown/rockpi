import requests
from bs4 import BeautifulSoup
import json
import types
import math
import urllib

'''
Amazon Products List Crawler:
1. Need to fake a browser
2. Ajax api url was form by two parts. Former is fixed : http://www.amazon.com/mn/search/ajax/, Later would be like ref=sr_pg_1 where 1 is the page number
3. Parmas :
   fromHash and qid are not necessary; 
   rh may refer to the category where start your search. So rh is fixed when you search in a certain category. Prepare it in advance.

rh:n:1055398,k:Buddhism
page:2
keywords:Buddhism
ie:UTF8
qid:1377655925
fromHash:/ref=sr_pg_1?rh=n%3A1055398%2Ck%3ABuddhism&keywords=Buddhism&ie=UTF8&qid=1377600110
section:ATF,BTF
fromApp:gp/search
fromPage:results
version:2

4. Below is a sample : 
'http://www.amazon.com/mn/search/ajax/ref=sr_pg_1?rh=n%3A1055398%2Ck%3ABuddhism&keywords=Buddhism&ie=UTF8&section=ATF,BTF&fromApp=gp%2Fsearch&fromPage=results&version=2'
'''

amazon_ajax_url = 'http://www.amazon.com/mn/search/ajax/'

s = requests.Session()
s.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:18.0) Gecko/20100101 Firefox/18.0',
    'Host': 'www.amazon.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate'})

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
    
    
    
    
    
    