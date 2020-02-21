from flask import Flask
import folium
import osmnx as ox

app = Flask(__name__)
@app.route('/')
def index():
    start_coords = (1.40527,103.90236) #punggol mrt
    folium_map = folium.Map(location=start_coords, tiles='Stamen Toner', zoom_start=50, width="75%", height="75%")
    place = "Northeast, Singapore, Singapore"
    hdb = ox.footprints_from_point(point=start_coords, distance=2000, footprint_type='building')
    hdb_points = hdb[hdb.building == 'residential']
    style_buildings = {'color':' #6C3483', 'fillColor': '#33FFC0 ', 'weight':'1', 'fillOpacity' : 0}
    folium.GeoJson(hdb_points,style_function=lambda x: style_buildings, tooltip='HDB').add_to(folium_map)
    return folium_map._repr_html_()

if __name__ == "__main__":
    app.run()



