import requests
from bs4 import BeautifulSoup
import json
import types

t_url = 'http://www.amazon.com/Japanese-Tanuki-Raccoon-Dog-Statue/dp/B003V1K2M6/ref=sr_1_50?s=home-garden&ie=UTF8&qid=1377583684&sr=1-50&keywords=Buddhism'
#t_url = 'http://www.amazon.com/Hand-Carved-Sitting-Buddha-Statue/dp/B001TOIF2G/ref=sr_1_49?s=home-garden&ie=UTF8&qid=1377583672&sr=1-49&keywords=Buddhism'


s = requests.Session()
s.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:18.0) Gecko/20100101 Firefox/18.0',
    'Host': 'www.amazon.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate'})

def parse_amazon_goods_detail(goods_url):
    try:
        ret = s.get(goods_url, timeout=3)
    except:
        print 'Parsr Error'
        return ()
    soup = BeautifulSoup(ret.text)
    
    goods_title = soup.find(id='btAsinTitle').string.strip()
    
    goods_image = soup.find(id='main-image')['rel']
    
    goods_price = soup.find(id='actualPriceValue').string.strip('$')
    
    goods_descrip = soup.find(id="productDescription").find('div','productDescriptionWrapper').contents[0].string.strip()
    
    tag_spec = soup.find(id='feature-bullets-atf')
    goods_spec = ''
    for row in tag_spec.find_all('li'):
        goods_spec += row.string + '\n'
    goods_spec = goods_spec.strip()
    
    # parse js code to get images
    js_start = ret.text.find("var colorImages")
    js_end = ret.text.find(";", js_start)
    js_start = ret.text.find('{',js_start)
    js_end = ret.text.rfind('}',js_start, js_end)
    json_image = json.loads(ret.text[js_start : js_end+1])
    list_image_groups = json_image['initial']
    
    goods_image = []
    image_types = (u'large',u'main',u'landing',u'thumb')
#    for group in list_image_groups:
    group = list_image_groups[0]
    for img_type in image_types:
        imgs = group[img_type]
        if type(imgs) == types.ListType:
            goods_image.append(list(imgs)[0] if imgs else None)
        else:
            goods_image.append(imgs)
    
    return (goods_title, goods_price, goods_descrip, goods_spec, goods_image)



def test():
    fout = open("C:\\Users\\Rock\\Desktop\\log.txt", "w")
    
    ama = parse_amazon_goods_detail(t_url)
    
    for ss in tuple(ama):
        fout.write(str(ss)+"\n\n")
        print ss,'\n'
    fout.close()


if __name__ == '__main__':
    test()