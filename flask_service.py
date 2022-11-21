import numpy as np
import pandas as pd
import os
import time
import json
import numpy as np
from flask import Flask, request, jsonify
import pickle
import pickle


app = Flask(__name__)

# Create route for each model

def bad_request(message):
    response = jsonify({'message': message})
    response.status_code = 400
    return response


"""
API runs a select model for PGA Success Prediction

Route: http://localhost:8080/api/predictPGASuccess
Request Type: POST

JSON request format:
    {
        "id" : _,
        "data" :{
            "Average Score": _,
            "Average SG Total": _,
            "Points": _
        "scaler": [MinMax, Standard, None]
        "model": _,
    }
Example request:
    {
        "id": 1,
        "data": {
            "Average Score": 70,
            "Average SG Total": 1.1,
            "Points": 700
        },
        "scaler": "MinMax",
        "model": "RidgeRegressor"
    }

returns: JSON object with id and prediction
        - If error occurs, a detailed JSON error message will be returned

"""
@app.route('/api/predictPGASuccess', methods=['POST'])
def predictPGASuccess():

    jsonObj = request.json

    # Check if JSON is passed with correct keys
    if not jsonObj: 
        return bad_request('Message must be JSON')

    if "id" not in jsonObj or "data" not in jsonObj or "scaler" not in jsonObj or "model" not in jsonObj:
        return bad_request('Missing JSON key in request, please refer to documentation')


    # Request ID
    req_id = str(jsonObj['id'])

    # Feature key validation 
    features = ['Average Score', 'Average SG Total', 'Points']
    # features = ["Rounds", "Fairway Percentage", "Avg Distance", "gir", "Average Putts", "Average Scrambling", "Average Score", "Points", "Wins", "Average SG Putts", "Average SG Total", "SG:OTT", "SG:APR", "SG:ARG"]

    feats = jsonObj['data']

    for featureName in features:
        if featureName not in feats:
            return bad_request('Missing [' + featureName + '] from JSON data object')

    for key in feats.keys():
        feats[key] = [float(feats[key])]

    # Scaler key validation
    scaler = str(jsonObj['scaler'])
    if scaler != "MinMax" and scaler != "Standard" and scaler != "None":
        return bad_request('Return valid scaler: MinMax, Standard, or None')
    
    # Load corresponding scaler and run fit on features
    if scaler == "MinMax":
        file = open('data/minMaxScaler.pkl', 'rb')
        scaler = pickle.load(file)
        file.close()
    elif scaler == "Standard":
        file = open('data/standardScaler.pkl', 'rb')
        scaler = pickle.load(file)
        file.close() 

    feats = scaler.transform(pd.DataFrame(feats))


    
    # Model key validation
    modelName = str(jsonObj['model'])
    modelPath = 'models/' + modelName + '.pkl'
    if os.path.exists(modelPath) == False:      
        return bad_request('Not a valid model name, select from models folder: DecisionTree, LinearRegressor, NN, ect.')
    
    
    # Load model and predict on data
    file = open(modelPath, 'rb')
    model = pickle.load(file)
    file.close()

    prediction = model.predict(feats)
    
    ret = {}
    ret['id'] = req_id
    ret['prediction'] = str(prediction[0])

    return json.dumps(ret) 


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080, debug=False)