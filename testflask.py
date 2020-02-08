from flask import Flask, render_template
from collections import deque, namedtuple
from flask import jsonify
import distrack as a


app = Flask(__name__)
@app.route('/')
def index():
    test = (a.dijsktra(a.graph, 'Punggol MRT', 'SIT'))
    return render_template("index.html",test=test)

if __name__ == "__main__":
    app.run()



