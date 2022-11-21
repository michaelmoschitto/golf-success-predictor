import numpy as np
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
Route runs a model for PGA Success Prediction

Route: http://localhost:8080/api/predict

JSON request object:
{
    "id" : _,
    "data" :{
        "Rounds": _,
        "Fairway Percentage": _,
        "Avg Distance": _,
        "gir": _,
        "Average Putts": _,
        "Average Scrambling": _,
        "Average Score": _,
        "Points": _,
        "Wins": _,
        "Average SG Putts": _,
        "Average SG Total": _,
        "SG:OTT": _,
        "SG:APR": _,
        "SG:ARG": _
    }
    "scaler": [MinMax, Standard, None]
    "model": _,
}

returns: JSON object with id and prediction
        - If error occurs, a details JSON error message

"""
@app.route('/api/predict',methods=['POST'])
def predict():
    if not request.json: 
        return bad_request('Message must be JSON')

    # Load model from pickle
    # Apply data transformations
    # Run predict 
    # Return json 
    req_id = str(request.json['id'])


    features = ["Rounds", "Fairway Percentage", "Avg Distance", "gir", "Average Putts", "Average Scrambling", "Average Score", "Points", "Wins", "Average SG Putts", "Average SG Total", "SG:OTT", "SG:APR", "SG:ARG"]
    
    
    feats = request.json['data']

    for featureName in features:
        if featureName not in feats:
            return bad_request('Missing [' + featureName + '] from JSON data object')


    scaler = str(request.json['scaler'])
    if scaler != "MinMax" or scaler != "Standard" or scaler != "None":
        return bad_request('Return valid scaler: MinMax, Standard, or None')


    for file in os.listdir('models/'):
        if file.endswith('.pkl'):

    model = str(request.json['model'])



    return '{"id": "' + req_id + '"}'


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080, debug=False)