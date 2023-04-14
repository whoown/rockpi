# coding=utf-8
# -*- coding: UTF-8 -*-
# USA Virtual MailBox address service such as AnytimeMailBox: https://www.anytimemailbox.com/l/usa
# This script is used for crawling all address from AnytimeMailBox and save to a file.
'''Dependencies''' 
# https://pypi.org/project/selenium/#files
# https://pypi.org/project/webdriver-manager/#files // Useless on windows platform 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os

# USA state infos. Just copy it from https://www.anytimemailbox.com/l/usa
usa_states = '''
Alabama 8
Alaska
Arizona 31
Arkansas 5
California 272
Colorado 27
Connecticut 8
DC 5
Delaware 16
Florida 152
Georgia 65
Hawaii 2
Idaho 3
Illinois 37
Indiana 10
Iowa 6
Kansas 7
Kentucky 3
Louisiana 14
Maine 3
Maryland 49
Massachusetts 14
Michigan 29
Minnesota 9
Mississippi 4
Missouri 6
Montana 4
Nebraska 3
Nevada 35
New Hampshire 3
New Jersey 43
New Mexico 3
New York 85
North Carolina 47
North Dakota
Ohio 25
Oklahoma 9
Oregon 32
Pennsylvania 25
South Carolina 20
South Dakota 2
Tennessee 15
Texas 199
Utah 3
Vermont
Virginia 28
Washington 35
West Virginia 3
Wisconsin 14
Wyoming 3
'''

# Download recently chrome driver from: 
# https://chromedriver.chromium.org/downloads
driver_path = 'D:\\Work\\github\\rockpi\\crawlers\\drivers\\chromedriver.exe'

def parse_usa_states():
    states = []
    for c in usa_states.split("\n"):
        if not c.strip():
            continue
        segs = c.split(" ")
        if len(segs) == 3:
            states.append(segs[0].lower()+"-"+segs[1].lower())
        elif len(segs) == 2 or len(segs) ==1:
            states.append(segs[0].lower())
    return states


def parse_single_address(data:str):
    lines = data.strip().split("\n")
    if len(lines) != 6:
        print('Address parse failed-1: %s'%data)
        return None
    street = lines[3]
    segs = lines[4].split(',')
    if len(segs) != 2:
        print('Address parse failed-2: %s'%data, segs)
        return None 
    city = segs[0].strip()
    segs = segs[1].strip().split(' ')
    if len(segs) != 2:
        print('Address parse failed-3: %s'%data, segs)
        return None
    state_in_short = segs[0].strip()
    postcode = segs[1].strip()
    return (state_in_short, city, street, postcode)


def crawl_state(driver, file_path, state):
    url = "https://www.anytimemailbox.com/l/usa/%s"%(state)
    print('------ Start crawling state: %s ------'%state)
    driver.get(url)
    driver.implicitly_wait(1)
    items = driver.find_elements(By.CLASS_NAME, 'theme-location-item')
    contents = []
    for item in items:
        address = parse_single_address(item.text)
        if not address:
            continue
        print('New address:',address)
        address_info = [state]+list(address)
        contents.append("|@|".join(address_info))

    # print(contents)
    data = "\n".join(contents)+"\n"
    with open(file_path, "a") as file:
        file.write(data)
    print('Crawling state %s finished.'%state)

def crawl_usa_states():
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service)
    file_name = "usa_addresses"
    if os.path.exists(file_name):
        print('Remove old state file.')
        os.remove(file_name)
    states = parse_usa_states()
    for c in states:
        crawl_state(driver, file_name, c)

if __name__ == '__main__':
    crawl_usa_states()

