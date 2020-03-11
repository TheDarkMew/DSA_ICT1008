import json
from math import *
import math
import httplib2 as http

def oneMap_apicall(search):

    headers={}
    method ='GET'
    body= ''
    SearchText = search
    h = http.Http()
    #is it possible to avoid searching based on numbers( bus stop number, block postal code)? MUST BE DAMN PRECISE FOR THIS FKING SEARCH
    response, content = h.request('https://developers.onemap.sg/commonapi/search?searchVal=' + SearchText + '&returnGeom=Y&getAddrDetails=Y&pageNum=1',method,body,headers)

    jsonObj = json.loads(content)
    return [hdb for hdb in jsonObj['results']]
def getLat(dict):
    for hdb in dict:
        return float(hdb['LATITUDE'])
def getLong(dict):
    for hdb in dict:
        return float(hdb['LONGITUDE'])
def convert(deg):
    return deg * (math.pi/180)

def test(dicts,newdict):
    earthradius = 6371
    punggol_lat = convert(1.3984)
    punggol_lon = convert(103.9072)

    count = 0
    for hdb in dicts:
        if hdb['LATITUDE'] and hdb['LONGITUDE']:
            count += 1
            print(hdb)
            newdict.append(hdb['SEARCHVAL'])
            newdict.append(hdb['LATITUDE'])
            newdict.append(hdb['LONGITUDE'])
    print(count)
def distance(lat1, lat2, lon1, lon2):
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # calculate the result ( based on km)
    return c * r

def spaceCheck(stringinput):
    return stringinput.replace(" ","%20")


newdict=[]
# User Input for Address
address = raw_input("Enter Address: ")
print(spaceCheck(address))

test(oneMap_apicall(spaceCheck(address)),  newdict)

print(newdict)