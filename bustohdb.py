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
def oneMap_areaCall(lat,long):
    headers= {}
    method = 'GET'
    body= ''
    getlat = str(lat)
    getlong= str(long)
    token ="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjQwMjgsInVzZXJfaWQiOjQwMjgsImVtYWlsIjoiam9lbHllbzE5OTRAZ21haWwuY29tIiwiZm9yZXZlciI6ZmFsc2UsImlzcyI6Imh0dHA6XC9cL29tMi5kZmUub25lbWFwLnNnXC9hcGlcL3YyXC91c2VyXC9zZXNzaW9uIiwiaWF0IjoxNTg0NTM1NDAwLCJleHAiOjE1ODQ5Njc0MDAsIm5iZiI6MTU4NDUzNTQwMCwianRpIjoiODgyMDljYzFkN2FiMTVlOTk3Y2NmYmE1YTQxYTE4MTkifQ.lH_38uJNpIFebKi4cC9vgNa9mkosu1cA0L5DOzqaQ2Q"
    h = http.Http()
    response, content = h.request("https://developers.onemap.sg/privateapi/commonsvc/revgeocode?location="+ getlat+"," +
                                 getlong+"&token="+token+"&buffer=500&addressType=HDB")
    jsonObj = json.loads(content)
    return [areaHdb for areaHdb in jsonObj['GeocodeInfo']]
def getLat(dict):
    for hdb in dict:
        return float(hdb['LATITUDE'])
def getLong(dict):
    for hdb in dict:
        return float(hdb['LONGITUDE'])
def getName(dict):
    for hdb in dict:
        return str(hdb['ADDRESS'])
def convert(deg):
    return deg * (math.pi/180)

#Does for oneMap_areaCall
def testArea(dicts,newdict):
    count = 0
    dicts.size
    for areaHdb in dicts:
        count+=1
        newdict.append(areaHdb['BUILDINGNAME'])
        newdict.append(areaHdb['BLOCK'])
        newdict.append(areaHdb['ROAD'])
        newdict.append(areaHdb['POSTALCODE'])
        newdict.append(areaHdb['LATITUDE'])
        newdict.append(areaHdb['LONGITUDE'])
    print(count)

#Does for oneMap_apiCall
def test(dicts,newdict):
    earthradius = 6371
    punggol_lat = convert(1.3984)
    punggol_lon = convert(103.9072)

    count = 0
    for hdb in dicts:
        if hdb['LATITUDE'] and hdb['LONGITUDE']:
            count += 1
            newdict.append(hdb['SEARCHVAL'])
            newdict.append(hdb['ADDRESS'])
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

#for checking space between the input ( unsure if i still need this since most bus stop codes would be used instead)
def spaceCheck(stringinput):
    return stringinput.replace(" ","%20")


#Appends the final stop of the list ( since last is the distance, so the append is from -2 ( which is last point / i believe need to change this to -3 to suit the point better)
def storeLast(route,store):
    store.append(route[-2])


#returns the busstop description after the data has been used since not all bus stops have the proper name so need to use this
def returnLast(store):
    busstop = store[0]
    return busstop


# gets the lat/long/bus codes via LIST ( not dict)
def getLatList(storeLast3):
    return storeLast3[2]
def getLongList(storeLast3):
    return storeLast3[1]
def getBusCode(storeLast3):
    return storeLast3[3]
#Matches the last stop to the list to search for bus stop code and its lat/long
def match(storeLast,storeLast2,storeLast3):
    for stop in storeLast2:
        if returnLast(storeLast) == stop:
            index = storeLast2.index(stop)
            storeLast3.append(storeLast2[index])   #Description
            storeLast3.append(storeLast2[index+1]) #Long
            storeLast3.append(storeLast2[index + 2]) #Lat
            storeLast3.append(storeLast2[index + 3]) #busstop code
    return storeLast3

#Distance adding but i think this is useless cause not added to the algorthim
def addUpDist(list1,list2):
    newDist= float(list1[-1][15:]) + float(list2)
    return newDist


def addBehind(list1, test):
    list1.insert(-2,test)
def check(list):
    return list

newdict=[]
newdict2=[]
# User Input for Address
#address = "824174"
#print(spaceCheck(address))
#test(oneMap_apicall(spaceCheck(address)),  newdict)
#print(newdict)

testArea(oneMap_areaCall(1.3984,103.9072),newdict)
print(newdict)