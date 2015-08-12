from amazon_goods_detail import parse_amazon_goods_detail
from amazon_goods_list import parse_amazon_goods_list
from peewee import *
from time import sleep, strptime


db = MySQLDatabase('rock', threadlocals=True, **{'host':'localhost','passwd':'123', 'user':'root'})

class Goods(Model):
    #_id = IntegerField(primary_key = True)
    _name = CharField()
    _price = FloatField(null = True)
    _description = TextField(null = True)
    _specification = TextField(null = True)
    _image_url_large = CharField(null = True)
    _image_url_main = CharField(null = True)
    _image_url_landing = CharField(null = True)
    _image_url_thumb = CharField(null = True)

    class Meta:
        database = db
        db_table = 'amazon'

def crawler_run():
    db.connect()
    if not Goods.table_exists():
        Goods.create_table()
    
    amazon_rh = 'n:1055398,k:Buddhism'
    keyword = 'Buddhism'
    goods_urls = []
    for page in range(1, 11):
        print 'Start archive page ',page 
        goods_urls += parse_amazon_goods_list(amazon_rh, keyword, page)
        sleep(10)
    
    print 'Amazon List archived. Url amounts = ', goods_urls.__len__()
    
    # (goods_title, goods_price, goods_descrip, goods_spec, goods_image)
    for goods in goods_urls:
        print 'Start parse : '+goods
        try:
            info = parse_amazon_goods_detail(goods)
            Goods.create(_name=info[0], _price=info[1], _description=info[2], _specification=info[3], _image_url_large=info[4][0], _image_url_main=info[4][1],_image_url_landing='',_image_url_thumb=info[4][3])
        except:
            print 'Failed parse : '+goods
            continue
        sleep(10)
    
    print 'Amazon Crawler Over'


if __name__ == '__main__':
    crawler_run()    