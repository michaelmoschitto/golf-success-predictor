import tensorflow as tf
import random
import numpy as np
import os
import time
import json
import numpy as np
from flask import Flask, request, jsonify
import pickle
import base64
from tensorflow import keras


app = Flask(__name__)

# Create route for each model


@app.route('/api/capture',methods=['POST'])
def predict():
    if not request.json: 
        abort(405)

    # Load model from pickle
    # Apply data transformations
    # Run predict 
    # Return json 
    
    req_id = str(request.json['id'])

    return '{"id": "' + req_id + '"}'


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080, debug=False)