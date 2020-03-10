# import xmltodict
# import untangle
import json
import urllib
import httplib2 as http
import requests


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
    bus_route_url = 'http://datamall2.mytransport.sg/ltaodataservice/BusRoutes'

    h = http.Http()
    results = []
    #Loop to run the API calls until the end of the dataset to get every bus route in Singapore
    while True:
        new_results = requests.get(bus_route_url, headers=headers, params={'$skip': len(results)}).json()['value']
        if new_results == []:
            break
        else:
            results += new_results

    # Save Results to file
    with open("north_bus_routes.json", "w") as outfile:
        # Saving jsonObj["d"]
        json.dump(results, outfile, sort_keys=True, indent=4,
                  ensure_ascii=False)


bus_routes_apicall()
