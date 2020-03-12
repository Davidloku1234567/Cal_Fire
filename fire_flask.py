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
    return render_template('form.html')

#submission page
@app.route('/submit')
# load in the form data from the incoming request
def submit():
    user_input = request.args

    date = []
        int(user_input['date']),
    ])
    return jsonify({'data' : data})
    # ref=pd.read_json('../Cal_Fire/preds.json', typ='dictionary')
    # model = pickle.load(open('assets/model.p', 'rb'))
    # preds = model.predict(X_test)
    # pred = round(preds[0],2)
    # return render_template('results.html', prediction=pred)
# manipulate data into a format that we pass to our model
# Call app.run(debug=True) when python script is called

if __name__ == '__main__': # if we run the file (app_starter.py) from the terminal
    app.run(debug=True)
