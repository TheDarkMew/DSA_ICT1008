from flask import Flask, render_template, request
from collections import deque, namedtuple
from flask import jsonify
import dijkstra as a
import dijkstrabusroute as b
import dijkstrawalkinghdb as c
import pandas as pd
import plotly_graph as g
import plotlyGrpah_LRT as gLRT
import plotlyGraph_BUS as gBUS
import plotlyGraph_WALK as gWALK
import folium
from folium import plugins

start_coords = (1.40527,103.90236) #punggol mrt
folium_map = folium.Map(location=start_coords, tiles='OpenStreetMap', zoom_start=50, width="100%", height="100%")
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
# Initialising Map
@app.route('/')
def index():
    data = pd.read_excel(r'HDBExcel2.xlsx')
    df = pd.DataFrame(data, columns=['punggol blk_no']) #COLUMN TITLE
    blkno = data['punggol blk_no'].tolist()  #GETTING ALL THE BLK NO FROM EXCEL FILE
    #print(blkno)
    folium_map.save('templates/folium_map.html')
    return render_template("index.html",blkno=blkno)

@app.route('/route', methods=['GET', 'POST'])
def route():
    if request.method == "POST":
        data = pd.read_excel(r'HDBExcel2.xlsx')
        df = pd.DataFrame(data, columns=['punggol blk_no'])  # COLUMN TITLE
        blkno = data['punggol blk_no'].tolist()  # GETTING ALL THE BLK NO FROM EXCEL FILE
        start = request.form.get("start", None)  # TAKING THE PARAMETERS
        end = request.form.get("end", None)  # TAKING THE PARAMETERS
        mode = request.form.get("mode", None)  # TAKING THE PARAMETERS
        path_coords = [] #storing coordinates for each node in path
        if (mode=="TRANSIT"):#BUSMODE
            start="Punggol Temp Int"
            test = (b.dijsktra(b.graph, start, end))
            gBUS.findRouteGraph(start, end)
            path_coords = b.get_path_coords(b.buslist,c.datahdb,test)
        elif (mode=="WALKING"):#WALKING MODE HDB-HDB
            start = "NE17 PTC Punggol"
            test = (c.dijsktra(c.graph, start, end))
            gWALK.findRouteGraph(start, end)
            path_coords = c.get_path_coords(c.datahdb,c.datamrt,test)
        else:
            test = (a.dijsktra(a.graph, start, end))
            gLRT.findRouteGraph(start, end)
            path_coords = a.get_path_coords(c.datahdb,a.datamrt,test)
        if "Not Possible" not in test[0]:
            folium_map = folium.Map(location=start_coords, tiles='OpenStreetMap', zoom_start=50, width="100%",
                                    height="100%")  # Reinitialise map to clear all previous markers
            for i in range(len(path_coords)):
                folium.CircleMarker(location=path_coords[i], tooltip=test[i], color='blue', fill=False).add_to(
                    folium_map)  # Place markers per node
            # folium.PolyLine(locations=path_coords, smooth_factor=0.1).add_to(folium_map)
            path_line = plugins.AntPath(locations=path_coords)  # Create path line between each nodes
            path_line.add_to(folium_map)
            folium_map.save("templates/folium_map.html")  # save to template for auto reload
        else:
            # Reinitialise map to clear all previous markers
            folium_map = folium.Map(location=start_coords, tiles='OpenStreetMap', zoom_start=50, width="100%", height="100%")
            folium_map.save('templates/folium_map.html')  # save to template for auto reload
        print(start)
        print(end)
        print(mode)
    return render_template("index.html",test=test,blkno=blkno)

@app.route('/folium_map')
def map():
    return render_template('folium_map.html')

if __name__ == "__main__":
    app.run()



