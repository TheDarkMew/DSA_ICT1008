import json
import csv
import pandas as pd
import numpy as np
import urllib.request as ur
import httplib2 as http

#hdb = pd.read_csv('datasets/hdb/resale-flat-prices-based-on-registration-date-from-jan-2017-onwards.csv',usecols=['town','block','street_name'])
jsonFilePath = 'datasets/hdb/hdbresale.json'
jsonWrite = 'punggolhdb.json'
searchHDB= []
storingCoords=[]




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

def spaceCheck(stringinput):
    return stringinput.replace(" ","%20")


def loopList(hdblist):
    for index in str(hdblist):
        print(index)

def test(dicts,newdict):
    for hdb in dicts:
          newdict.append(hdb)
          

def readBus():
    punggolhdb={}
    hdbinfo = json.loads(open(jsonFilePath).read())
    for hdb in hdbinfo:
        if hdb['town'] == 'PUNGGOL':
            id = 'Results'
            town =(hdb['town'])
            block =(hdb['block'])
            street =(hdb['street_name'])
            punggolhdb[id] = town,block,street
    
    with open(jsonWrite,'w') as jsonFile:
        jsonFile.write(json.dumps(punggolhdb,indent=4))
        
readBus()