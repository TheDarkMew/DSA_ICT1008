from flask import Flask, render_template, request
from collections import deque, namedtuple
from flask import jsonify
import dijkstra as a
import pandas as pd

app = Flask(__name__)
@app.route('/')
def index():
    data = pd.read_excel(r'hdb.xlsx')
    df = pd.DataFrame(data, columns=['punggol blk_no']) #COLUMN TITLE
    blkno = data['punggol blk_no'].tolist()  #GETTING ALL THE BLK NO FROM EXCEL FILE
    #print(blkno)
    return render_template("index.html",blkno=blkno)

@app.route('/route', methods=['GET', 'POST'])
def route():
    if request.method == "POST":
        data = pd.read_excel(r'hdb.xlsx')
        df = pd.DataFrame(data, columns=['punggol blk_no'])  # COLUMN TITLE
        blkno = data['punggol blk_no'].tolist()  # GETTING ALL THE BLK NO FROM EXCEL FILE
        start = request.form.get("start", None)  # TAKING THE PARAMETERS
        end = request.form.get("end", None)  # TAKING THE PARAMETERS
        mode = request.form.get("mode", None)  # TAKING THE PARAMETERS
        test = (a.dijsktra(a.graph, start, end))
        print(start)
        print(end)
        print(mode)
    return render_template("index.html",test=test,blkno=blkno)


if __name__ == "__main__":
    app.run()



