# imports
import pandas as pd
import json
import pickle
import numpy as np
from flask import Flask, request, render_template, jsonify, Response

# initialize the flask app
app = Flask('fire_flask')

#form page
@app.route('/fire_form')

def form():
    return render_template('fire_form.html')

#submission page
@app.route('/submit')

def submit():
    user_input = request.args

    date = user_input['date']
    date_present = date[5:]
    ref=pd.read_json('../Cal_Fire/preds.json', typ='dictionary')


    pred = ref[date].round()
    return render_template('results.html', pred=pred, date=date_present)


if __name__ == '__main__': # if we run the file (fire_flask.py) from the terminal
    app.run(debug=True)
