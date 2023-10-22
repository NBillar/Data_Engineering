import os
import json
import sys
import joblib
import pandas as pd
from flask import jsonify
from google.cloud import storage


def predict_wine_quality(request):
    """
    This function will be executed when the endpoint is called
    """
    # extract the request body
    request_json = request.get_json()
    # logging the request body
    print("Request received : {}".format(request_json))

    # extract the request parameters
    # => Nodig?
    fixed_acidity = request_json['fixed_acidity']
    volatile_acidity = request_json['volatile_acidity']
    citric_acid = request_json['citric_acid']
    residual_sugar = request_json['residual_sugar']
    chlorides = request_json['chlorides']
    free_sulfur_dioxide = request_json['free_sulfur_dioxide']
    total_sulfur_dioxide = request_json['total_sulfur_dioxide']
    density = request_json['density']
    pH = request_json['pH']
    sulphates = request_json['sulphates']
    alcohol = request_json['alcohol']

    # load the model from cloud storage

    #---------------------------------
    ## => Waar staat de model file?
    model = joblib.load('X')
    #---------------------------------

    # make prediction
    df = pd.read_json(json.dumps(request_json), orient='records')
    print(df, file=sys.stdout)
    y_pred = model.predict(df)

    # return the response
    return jsonify({'result': y_pred[0].tolist()})
