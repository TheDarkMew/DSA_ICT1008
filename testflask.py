from flask import Flask
import folium
import osmnx as ox
import networkx as nx
import overpy

app = Flask(__name__)
@app.route('/')
def index():
    #126D
    # overpass = overpy.Overpass()
    # result = overpass.query("""
    #     node["name"="Singapore"];node(around:3000,1.40527,103.90236)["highway"="bus_stop"];
    #     out;
    #     """)
    start_coords = (1.40527,103.90236) #punggol mrt
    folium_map = folium.Map(location=start_coords, tiles='OpenStreetMap', zoom_start=50, width="75%", height="75%")
    # hdb = ox.footprints_from_point(point=start_coords, distance=2000, footprint_type='building')
    # dataset = ox.footprints_from_point(point=start_coords, distance=2000)
    # hdb_points = dataset[dataset.building == 'residential']
    # print(hdb_points.columns)
    # print(hdb_points.loc[hdb_points['name'] == "Blk 126A",["geometry"]])
    # style_buildings = {'color':' #6C3483', 'fillColor': '#33FFC0 ', 'weight':'1', 'fillOpacity' : 0}
    # folium.GeoJson(hdb_points,style_function=lambda x: style_buildings, tooltip='HDB').add_to(folium_map)
    # for node in result.nodes:
    #     folium.Marker(location=[node.lat,node.lon],tooltip=node.id).add_to(folium_map)

    class Node:
        def __init__(self, coords, name):
            self.coordinates = coords
            self.name = name

    node_1 = Node((1.40527,103.90236), "First")
    node_2 = Node((1.4051328, 103.9027777), "Second")
    node_3 = Node((1.4040774, 103.9048174), "Third")
    node_4 = Node((1.4019230, 103.9078590), "Fourth")
    node_5 = Node((1.4023149, 103.9078645), "Fifth")
    node_6 = Node((1.4026846, 103.9081196), "Sixth")
    node_7 = Node((1.4031324, 103.9082255), "Seventh")
    node_list = [node_1,node_2,node_3,node_4,node_5,node_6,node_7]
    route_locations = []
    for node in node_list:
        route_locations.append(node.coordinates)
        folium.CircleMarker(location=node.coordinates, tooltip=node.name, color='crimson', fill=False).add_to(folium_map)
    folium.PolyLine(locations=route_locations, tooltip="Shortest Path",smooth_factor=0.1).add_to(folium_map)
    return folium_map._repr_html_()


if __name__ == "__main__":
    app.run()



