import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle

with open('./titanic.pkl', 'rb') as modelo_pkl:
    model_ = pickle.load(modelo_pkl)

app = Flask('app')
showPredictions = None


@app.route('/')
def home():
    return render_template("/static/index.html", showPredictions=None)


@app.route('/predict', methods=['GET'])
def predict():

    # TODO: add all required params
    input = {
        'Age': request.args['Age'],
        'Fare': request.args['Fare'],
        'Parch': request.args['Parch'],
        'SibSp': request.args['SibSp'],
        'Embarked_Q': 0,
        'Embarked_S': 0,
        'Pclass_2': 0,
        'Pclass_3': 0,
        'Sex_male': 0
    }

    input = pd.DataFrame.from_dict(input, orient='index').T

    response = model_.predict(input)

    ## Console response
    print('RESPUESTA:', response)

    return(response)
