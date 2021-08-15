import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle
# modelo predictor
with open('./models/titanic.pkl', 'rb') as modelo_pkl:
    model = pickle.load(modelo_pkl)
# scalador
with open('./models/titanic_scaler.pkl', 'rb') as modelo_pkl:
    model_scaler = pickle.load(modelo_pkl)

app = Flask('app')
showPredictions = None

clases = [
    {
        'clase': 1,
        'descripcion': 'Primera Clase',
        'cabinas': [
            {'tipo': 'A', 'valor': 41.2443},
            {'tipo': 'B', 'valor': 122.3831},
            {'tipo': 'C', 'valor': 107.9266},
            {'tipo': 'D', 'valor': 58.9191},
            {'tipo': 'E', 'valor': 63.4647},
            {'tipo': 'F', 'valor': 0},
            {'tipo': 'G', 'valor': 0}
        ]
    },
    {
        'clase': 2,
        'descripcion': 'Segunda Clase',
        'cabinas': [
            {'tipo': 'A', 'valor': 0},
            {'tipo': 'B', 'valor': 0},
            {'tipo': 'C', 'valor': 0},
            {'tipo': 'D', 'valor': 13.5958},
            {'tipo': 'E', 'valor': 11.5875},
            {'tipo': 'F', 'valor': 23.4231},
            {'tipo': 'G', 'valor': 0}
        ]
    },
    {
        'clase': 3,
        'descripcion': 'Tercera Clase',
        'cabinas': [
            {'tipo': 'A', 'valor': 0},
            {'tipo': 'B', 'valor': 0},
            {'tipo': 'C', 'valor': 0},
            {'tipo': 'D', 'valor': 0},
            {'tipo': 'E', 'valor': 11.0000},
            {'tipo': 'F', 'valor': 9.3958},
            {'tipo': 'G', 'valor': 14.2050}
        ]
    }
]


@app.route('/')
def home():
    return render_template("index.html", showPredictions=None)


@app.route('/classes')
def get_classes():
    return jsonify(clases)


@app.route('/predict', methods=['GET'])
def predict():

    input = {
        'Age': request.args['Age'],
        'Fare': 0,
        'Parch': request.args['Parch'],
        'SibSp': request.args['SibSp'],
        'Embarked_Q': 0,
        'Embarked_S': 0,
        'Pclass_2': 0,
        'Pclass_3': 0,
        'Sex_male': request.args['Sex_male'],
        'Embarked': request.args['Embarked'],
        'Class': request.args['Class']
    }

    input = pd.DataFrame.from_dict(input, orient='index').T

    # import joblib
    from sklearn.preprocessing import MinMaxScaler
    model_scaler.clip = False
    input.iloc[:, [0, 1, 2, 3]] = model_scaler.transform(
        input.iloc[:, [0, 1, 2, 3]])
    input['Embarked_Q'] = [1 if x == 'Q' else 0 for x in input['Embarked']]
    input['Embarked_S'] = [1 if x == 'S' else 0 for x in input['Embarked']]
    input['Pclass_2'] = [1 if x == 2 else 0 for x in input['Class']]
    input['Pclass_3'] = [1 if x == 3 else 0 for x in input['Class']]
    print(input)
    input.drop(['Embarked', 'Class'], axis=1, inplace=True)

    response = model.predict(input)

    # print('RESPUESTA', response[0], )

    chance = model.predict_proba(input)
    # para añadir la probabilidad de supervivencia
    print('Probabilidad de sobrevivir', round(chance[0][1]*100, 1) )

    percentile = round(chance[0][1]*100, 1)

    survived = percentile > 50  # si es mayor a 50 es igual a True, y sino es False

    return jsonify({
        'result': survived and 'Felicidades, sobrevivirias al Titanic' or 'Lo lamentamos, no hubieras sobrevivido al titanic',
        'survived': survived and True or False,
        'percentile': percentile
    })


if __name__ == '__main__':
    app.run(debug=True)

# for pure use of the model


@app.route('/usemodel', methods=['GET'])
def use_model():

    input = {
        'Age': 8,
        'Fare': 23,
        'Parch': 3,
        'SibSp': 4,
        'Embarked_Q': 0,
        'Embarked_S': 0,
        'Pclass_2': 0,
        'Pclass_3': 0,
        'Sex_male': 'M',
        'Embarked': 'Q',
        'Class': 'Tercera'
    }
    # request.args['Embarked'], no me toma esto cuando lo escribo :/
    # request.args['Class'], pasa lo mismo que el caso anterior, de especificarlo no me lo toma

    input = pd.DataFrame.from_dict(input, orient='index').T

    # import joblib
    from sklearn.preprocessing import MinMaxScaler
    model_scaler.clip = False
    input.iloc[:, [0, 1, 2, 3]] = model_scaler.transform(
        input.iloc[:, [0, 1, 2, 3]])
    input['Embarked_Q'] = [1 if x == 'Q' else 0 for x in input['Embarked']]
    input['Embarked_S'] = [1 if x == 'S' else 0 for x in input['Embarked']]
    input['Pclass_2'] = [1 if x == 'Segunda' else 0 for x in input['Class']]
    input['Pclass_3'] = [1 if x == 'Tercera' else 0 for x in input['Class']]
    print(input)
    input.drop(['Embarked', 'Class'], axis=1, inplace=True)

    response = model.predict(input)

    # print('RESPUESTA', response[0], )

    chance = model.predict_proba(input)
    # para añadir la probabilidad de supervivencia
    print('Probabilidad de sobrevivir', chance[0][1])

    if response[0] == 1.0:
        return jsonify({'result': 'Felicidades, sobrevivirias al Titanic', "survived": True})
    else:
        return jsonify({'result': 'Lo lamentamos, no hubieras sobrevivido al titanic', "survived": False})
