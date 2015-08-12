#Get wallpages from this site : http://www.allmacwallpaper.com/?home=1#
import requests
import re
import Queue
import threading
from bs4 import BeautifulSoup
from threadpool import ThreadPool
from threadpool import WorkRequest

site_host = "http://www.allmacwallpaper.com"
site_url = "http://www.allmacwallpaper.com/mac-wallpapers/Date/%(page_id)d?home=1"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
    'Host': 'www.allmacwallpaper.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate'}

session = requests.Session()
session.headers.update(headers)

tiny__pool = ThreadPool(6)
big_pool = ThreadPool(4)

failed_page_ids = []
image_count = 0
image_folder_small = "C:\\Users\\Rock\\Desktop\\small"
image_folder_large = "C:\\Users\\Rock\\Desktop\\large"


def run():
    for i in range(10):
        t = threading.Thread(target=worker, name="Thread"+str(i))
        t.daemon = True
        t.start()
     
    for i in range(1, 330):
        url = site_url%{'page_id':i}
        process_per_page(url)
        queue.join()       # block until all tasks are done
        
def process_per_page(url):
    global image_count
    #print url
    try:
        ret = session.get(url, timeout=3)
    except:
        print ''
        return ()
    
    #print ret.text
    soup = BeautifulSoup(ret.text)
    for dl in soup.find_all("dl"):
        dt = dl.find("dt")
        if dt and dt.find("a"):
            image_url = (dt.find("a"))['href']
            res = process_per_image_page(site_host+image_url)
            if res and (res[0] or res[1]):
                image_count += 1 
                load_image_and_save(res[0], 0)
                load_image_and_save(res[1], 1)


def process_per_image_page(url):
    try:
        ret = session.get(url, timeout=3)
    except:
        return (None, None)
    soup = BeautifulSoup(ret.text)
    tag_div = soup.find("div", {"class":"resolution clearfix"})
    if not tag_div:
        return (None, None)
    tag_divs = tag_div.find_all("div")
    ret = [None, None]
    for div in tag_divs:
        list_a = div.find_all("a")
        if not list_a:
            continue
        for a in list_a:
            image_summary, image_url = None, None
            try:
                image_summary = a.contents[0].string
                image_url = site_host + a['href']
            except:
                pass
            #print image_summary
            if image_summary == "Retina MacBook Pro 13-inch (2560x1600)":
                ret[0] = image_url
            elif image_summary == "Retina MacBook Pro 13-inch (2560x1600)" :
                ret[1] = image_url
    return tuple(ret)


###############################################
#Load Image and save to folder
###############################################

def load_image_and_save(url, is_large_image):
    image_name_list = re.findall("/(\d+)-\d+\.jpg", str(url))
    image_name = None
    if image_name_list:
        image_name = image_name_list[-1]
    if not image_name:
        return
    if is_large_image:
        image_path = image_folder_large + "\\"+image_name+".jpg"
    else:
        image_path = image_folder_small + "\\"+image_name+".jpg"
    
    job = WorkRequest(download_image, (url, image_path))
    if is_large_image:
        #big_pool.putRequest(job)
        pass
    else:
        #tiny__pool.putRequest(job)
        queue.put((url, image_path))
        pass

queue = Queue.Queue(10000000)

def worker():
    while True:
        print 'Job runing in '+threading.currentThread().name+'. Total has '+str(queue.qsize()), str(queue.maxsize)
        item = queue.get()
        download_image(item)
        queue.task_done()
    
def download_image(arg):
    url = arg[0]
    image_path = arg[1]
    print 'Start in '+threading.currentThread().name+" for "+url
    try:
        ret = session.get(url, timeout=60)
        fout = open(image_path, "wb")
        fout.write(ret.content)
        fout.flush()
        fout.close()
        print "Done "+image_path
    except:
        print 'Download image failed. url= '+url

if __name__ == '__main__':
    run();