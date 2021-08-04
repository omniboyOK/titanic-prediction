import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle
# modelo predictor
with open('./titanic.pkl', 'rb') as modelo_pkl:
    model = pickle.load(modelo_pkl)
# scalador
with open('./titanic_scaler.pkl', 'rb') as modelo_pkl:
    model_scaler = pickle.load(modelo_pkl)

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
        'Sex_male': request.args['Sex_male']
    }

    input = pd.DataFrame.from_dict(input, orient='index').T

    # import joblib
    from sklearn.preprocessing import MinMaxScaler
    model_scaler.clip = False
    input.iloc[:, [0, 1, 2, 3]] = model_scaler.transform(
        input.iloc[:, [0, 1, 2, 3]])
    # hasta poder reparar lo del genero 1:Masculino 0:Femenino
    input.iloc[:, 8] = 1
    print(input.Sex_male)
    print(input)
    response = model.predict(input)

    # print('RESPUESTA', response[0], )

    if response[0] == 1.0:
        return jsonify({'result': 'Felicidades, sobrevivirias al Titanic', "survived": True})
    else:
        return jsonify({'result': 'Lo lamentamos, no hubieras sobrevivido al titanic', "survived": False})


if __name__ == '__main__':
    app.run(debug=True)
