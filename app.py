import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask('app')
model_ = pickle.load( open('./titanic.pkl','wb') )
showPredictions = None


@app.route('/')
def home():
    return render_template("index.html", showPredictions=None)

@app.route('/predict', methods=['GET'])
def predict():
    ## TODO: add all required params
    input = {
        'Age': request.args['Age'],
        'Fare': request.args['Fare'],
        'Parch': request.args['Parch'] ,
        'SibSp': request.args['SibSp'],
        'Embarked_Q': 0,
        'Embarked_S': 0,
        'Pclass_2': 0,
        'Pclass_3': 0,
        'Sex_male': 0
    }

    input = pd.DataFrame.from_dict(input, orient='index').T

    response = model_.predict( input )
    # print(response)
    return(response)

