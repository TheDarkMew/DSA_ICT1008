# import xmltodict
# import untangle
import json
import urllib
import httplib2 as http


headers = {'AccountKey': 'xGDPz1wIT2uzuczm3UoZ5Q==', 'accept': 'application/json'}
method = 'GET'
body = ''

h = http.Http()

response, content = h.request('http://datamall2.mytransport.sg/ltaodataservice/BusStops?$skip=3000',method,body,headers)

jsonObj = json.loads(content)
print(json.dumps(jsonObj,sort_keys=True, indent=4))
