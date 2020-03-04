# import xmltodict
# import untangle
import json
import urllib
import httplib2 as http


def bus_stops_apicall():
    headers = {'AccountKey': 'xGDPz1wIT2uzuczm3UoZ5Q==', 'accept': 'application/json'}
    method = 'GET'
    body = ''

    h = http.Http()

    response, content = h.request('http://datamall2.mytransport.sg/ltaodataservice/BusStops?$skip=4000', method, body,
                                  headers)

    jsonObj = json.loads(content)
    print(json.dumps(jsonObj, sort_keys=True, indent=4))

    # Save Results to file
    with open("north_bus_stops_part3.json", "w") as outfile:
        # Saving jsonObj["d"]
        json.dump(jsonObj, outfile, sort_keys=True, indent=4,
                  ensure_ascii=False)


def bus_routes_apicall():
    headers = {'AccountKey': 'xGDPz1wIT2uzuczm3UoZ5Q==', 'accept': 'application/json'}
    method = 'GET'
    body = ''

    h = http.Http()

    response, content = h.request('http://datamall2.mytransport.sg/ltaodataservice/BusRoutes?$skip=3000', method, body,
                                  headers)

    jsonObj = json.loads(content)
    print(json.dumps(jsonObj, sort_keys=True, indent=4))


bus_routes_apicall()
