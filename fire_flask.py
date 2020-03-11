# imports
import pickle
import numpy as np
from flask import Flask, request, render_template, jsonify, Response

# initialize the flask app
app = Flask('myApp')

# route 1: hello world
@app.route('/')

# return a simple string
def home():
    return 'hello from Flask!'

# route 2: return a 'web page'

@app.route('/hc_page') # hard-coded page
# return some hard-coded html
def hc_page():
    return '<html><body><h1>This is a hard coded page!</h1><p>Here is some hard-coded content. Isn\'t it pretty?</p></body></html>'

# route 3: return some data
@app.route('/hc_page.json')
# create some data to return as json
def hc_json():
    the_best = {
    'food' : 'breakfast tacos',
    'movie': 'inception',
    'mineral water': 'dumb water',
    }
    return jsonify(the_best)
# use flask's jsonify function to return the data as well as a 200 status code
@app.route('/form')
# route 4: show a form to the user
def form():
    return render_template('form.html')
# use flask's render_template function to display an html page
# route 5: accept the form submission and do something fancy with it
@app.route('/submit')
# load in the form data from the incoming request
def submit():
    user_input = request.args

    X_test = np.array([
        int(user_input['OverallQual']),
        int(user_input['FullBath']),
        int(user_input['GarageArea']),
        int(user_input['LotArea'])
    ]).reshape(1, -1) # turns it into a 1x4 matrix

    model = pickle.load(open('assets/model.p', 'rb'))
    preds = model.predict(X_test)
    pred = round(preds[0],2)
    return render_template('results.html', prediction=pred)
# manipulate data into a format that we pass to our model
# Call app.run(debug=True) when python script is called

if __name__ == '__main__': # if we run the file (app_starter.py) from the terminal
    app.run(debug=True)
