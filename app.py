import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask('app')
model = None ## add model here
showPredictions = None


@app.route('/')
def home():
    return render_template("index.html", showPredictions=None)


@app.route('/predict', methods=['GET'])
def predict():
    ## TODO: add all required params
    input = {
        'age': request.args['age']
    }
