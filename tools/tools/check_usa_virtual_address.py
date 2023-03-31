# coding=utf-8
# -*- coding: UTF-8 -*-
__author__ = 'Rock'
# USA Virtual MailBox address service such as AnytimeMailBox: https://www.anytimemailbox.com/l/usa/california
# Use Smarty API to check whether the address is commercial or retential ?  Refer to : https://www.smarty.com/docs/cloud/us-street-api
#
import requests
import json
AUTH_ID = "61f0461b-fb8c-1f9d-7872-50811f52941e"
AUTI_TOKEN = "Q8DfO9ItaLKzaZ7u2T3y"

PROXIES = { 
              "http"  : "http://127.0.0.1:10809", 
              "https" : "http://127.0.0.1:10809", 
        }

def maps_get(m, keys):
    if not m:
        return None 
    v = m
    try:
        for k in keys:
            if v.get(k) != None:
                v = v.get(k)
            else:
                return None 
    except Exception as e:
        print("maps_get failed:",e)
        return None 
    return v

def check_address(street, city, state, zipcode):
    api = "https://us-street.api.smartystreets.com/street-address"
    params = {"auth-id":AUTH_ID, "auth-token":AUTI_TOKEN}
    street = street.strip()
    city = city.strip()
    state = state.strip()
    zipcode = zipcode.strip()
    if street:
        params["street"] = street
    if city:
        params["city"] = city
    if state:
        params["state"] = state
    if zipcode:
        params["zipcode"] = zipcode
    json_data = []
    try:
        resp = requests.get(api, params=params, proxies=PROXIES)
        json_data = resp.json()
        if not json_data:
            return None 
    except Exception as e:
        print("check_address failed:", e)
    
    data = json_data[0]
    rdi = maps_get(data,["metadata","rdi"])
    cmra = maps_get(data,["analysis","dpv_cmra"])
    vacant = maps_get(data,["analysis","dpv_vacant"])
    no_stat = maps_get(data,["analysis","dpv_no_stat"])
    return (rdi,cmra,vacant,no_stat)


########################

data = '''[{"input_index": 0, "candidate_index": 0, "delivery_line_1": "310 Flanders Rd", "last_line": "East Lyme CT 06333-1758", "delivery_point_barcode": "063331758996", "components": {"primary_number": "310", "street_name": "Flanders", "street_suffix": "Rd", "city_name": "East Lyme", "default_city_name": "East Lyme", "state_abbreviation": "CT", "zipcode": "06333", "plus4_code": "1758", "delivery_point": "99", "delivery_point_check_digit": "6"}, "metadata": {"record_type": "H", "zip_type": "Standard", "county_fips": "09011", "county_name": "New London", "carrier_route": "R006", "congressional_district": "02", "building_default_indicator": "Y", "rdi": "Residential", "elot_sequence": "0025", "elot_sort": "A", "latitude": 41.36357, "longitude": -72.20936, "precision": "Zip9", "time_zone": "Eastern", "utc_offset": -5, "dst": true}, "analysis": {"dpv_match_code": "D", "dpv_footnotes": "AAN1", "dpv_cmra": "N", "dpv_vacant": "N", "dpv_no_stat": "Y", "active": "Y", "footnotes": "LI#H#", "lacslink_code": "00", "lacslink_indicator": "N"}}]'''
if __name__ == '__main__':
    # res = check_address("310 Flanders Rd","East Lyme","CT","06333")
    # print(res)
    url ="https://www.anytimemailbox.com/l/usa/arizona"
    print(requests.get(url, proxies=PROXIES).text)

