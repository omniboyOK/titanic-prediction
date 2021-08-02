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
    return render_template("index.html", showPredictions=None)


@app.route('/predict', methods=['GET'])
def predict():
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

    print('RESPUESTA', response[0])

    if response[0] == 1.0:
        return jsonify({'result': 'Felicidades, sobrevivirias al Titanic'})
    else:
        return jsonify({'result': 'Lo lamentamos, no hubieras sobrevivido al titanic'})


if __name__ == '__main__':
    app.run(debug=True)
