from flask import Flask, render_template
from collections import deque, namedtuple
from flask import jsonify
import distrack as a
import folium

app = Flask(__name__)
@app.route('/')
def index():
    # test = (a.dijsktra(a.graph, 'Punggol MRT', 'SIT'))
    # return render_template("index.html",test=test)
    start_coords = (1.40527,103.90236) #punggol mrt
    folium_map = folium.Map(location=start_coords, zoom_start=50, width="75%", height="75%")

    return folium_map._repr_html_()

if __name__ == "__main__":
    app.run()



