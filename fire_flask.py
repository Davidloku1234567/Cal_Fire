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
# load in the form data from the incoming request
def submit():
    user_input = request.args

    date = user_input['date']
    date_present = date[5:]
    # date = jsonify({'date' : date})
    ref=pd.read_json('../Cal_Fire/preds.json', typ='dictionary')
    # model = pickle.load(open('assets/model.p', 'rb'))
    # preds = model.predict(X_test)

    pred = ref[date].round()
    return render_template('results.html', pred=pred, date=date_present)
# manipulate data into a format that we pass to our model
# Call app.run(debug=True) when python script is called

if __name__ == '__main__': # if we run the file (app_starter.py) from the terminal
    app.run(debug=True)
