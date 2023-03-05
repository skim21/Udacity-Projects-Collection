import pandas as pd

from flask import Flask
from flask import render_template, request, jsonify

import os
import sys
cwd = os.getcwd()
sys.path.append(cwd)

import piv_main
import ast

app = Flask(__name__)


# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    
    # render web page
    return render_template('master.html')


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input in query
    query = request.args.get('query', '') 
    query = query.replace('%5B', '[').replace('%5D',']')
    query = ast.literal_eval(query)
    # use model to predict classification for query
    no_valves, total, valves, n = piv_main.main(query)

    # This will render the go.html Please see that file. 
    return render_template(
        'go.html',
        query = query,
        no_valves = no_valves, 
        total = total, 
        valves = valves, 
        n = n
    )


def main():
    app.run(host='0.0.0.0', port=3000, debug=True)

if __name__ == '__main__':  
    main()