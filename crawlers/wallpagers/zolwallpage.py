# Get wallpages from this site : http://www.allmacwallpaper.com/?home=1#
import requests
import re
import Queue
import threading
from bs4 import BeautifulSoup
from threadpool import ThreadPool
from threadpool import WorkRequest

site_host = "http://desk.zol.com.cn/pc/%(page_id)d.html"
host = "http://desk.zol.com.cn";
site_url = "http://www.allmacwallpaper.com/mac-wallpapers/Date/%(page_id)d?home=1"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
    'Host': 'desk.zol.com.cn',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate'}

session = requests.Session()
session.headers.update(headers)

load_session = requests.Session()
load_headers = headers.copy()
print(load_headers)
load_headers['Host'] = "b.zol-img.com.cn"
load_session.headers.update(load_headers)

tiny__pool = ThreadPool(6)
big_pool = ThreadPool(4)

failed_page_ids = []
image_count = 0
image_download_folder = r"C:\Users\Rock\Desktop\image"

max_page_id = 306

current_page_index = -1


def run():
    for i in range(10):
        t = threading.Thread(target=worker, name="Thread" + str(i))
        t.daemon = True
        t.start()

    global current_page_index
    for i in range(1, max_page_id + 1):
        current_page_index = i;
        url = site_host % {'page_id': i}
        process_per_page(url)
        queue.join()  # block until all tasks are done


def process_per_page(url):
    global image_count
    # print url
    try:
        ret = session.get(url, timeout=3)
    except:
        print ''
        return

    # print ret.text
    soup = BeautifulSoup(ret.text)
    for ul in soup.find_all("ul", attrs={"class": "pic-list2  clearfix"}):
        for a in ul.find_all("a"):
            wallpage_url = host + a['href']
            process_per_image_page(wallpage_url)


def process_per_image_page(url):
    try:
        ret = session.get(url, timeout=3)
    except:
        return (None, None)
    soup = BeautifulSoup(ret.text)
    tag_ul = soup.find("ul", {"id": "showImg"})
    if not tag_ul:
        return (None, None)
    for a in tag_ul.find_all("a"):
        image_page_url = host + a['href']
        try:
            ret = session.get(image_page_url, timeout=3)
        except:
            continue
        soup = BeautifulSoup(ret.text)
        tag_dl = soup.find("dl", {"class": "model wallpaper-down clearfix"})
        if tag_dl:
            first_a = tag_dl.find("a", {"target": "_blank"})
            if first_a:
                image_url = host + first_a['href']
                load_image_and_save(image_url)

    return tuple(ret)


###############################################
# Load Image and save to folder
###############################################

def load_image_and_save(url):
    if not url:
        return
    try:
        ret = session.get(url, timeout=3);
    except:
        return
    soup = BeautifulSoup(ret.text)
    tag_image = soup.find("img")
    if tag_image:
        image_url = tag_image['src']
        image_name_list = re.findall("/(\d+)\.jpg", str(image_url))
        image_name = None
        if image_name_list:
            image_name = image_name_list[-1]
        if not image_name:
            return
        image_path = image_download_folder + "\\" + image_name + ".jpg"
        queue.put((image_url, image_path))

        # if is_large_image:
        #     # big_pool.putRequest(job)
        #     pass
        # else:
        #     # tiny__pool.putRequest(job)
        #     queue.put((url, image_path))


queue = Queue.Queue(10000000)


def worker():
    while True:
        print 'Job runing in ' + threading.currentThread().name + '. Total has ' + str(queue.qsize()), str(
            queue.maxsize)
        item = queue.get()
        download_image(item)
        queue.task_done()


def download_image(arg):
    url = arg[0]
    image_path = arg[1]
    global current_page_index
    print 'Start in ' + threading.currentThread().name + " for " + url
    try:
        ret = load_session.get(url, timeout=60)
        fout = open(image_path, "wb")
        fout.write(ret.content)
        fout.flush()
        fout.close()
        print "Done " + image_path + "  From: ", current_page_index
    except:
        print 'Download image failed. url= ' + url


if __name__ == '__main__':
    run()

