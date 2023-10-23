import os
import json
import sys
import joblib
import pandas as pd
from flask import jsonify
from google.cloud import storage
import pickle
import re
from io import StringIO


def predict_wine_quality(request, PROJECT_ID):
    """
    This function will be executed when the endpoint is called
    """
    # extract the request body
    request_json = request.get_json()

    # logging the request body
    print("Request received : {}".format(request_json))

    # extract the request parameters
    # => Nodig?
    fixed_acidity = request_json["fixed_acidity"]
    volatile_acidity = request_json["volatile_acidity"]
    citric_acid = request_json["citric_acid"]
    residual_sugar = request_json["residual_sugar"]
    chlorides = request_json["chlorides"]
    free_sulfur_dioxide = request_json["free_sulfur_dioxide"]
    total_sulfur_dioxide = request_json["total_sulfur_dioxide"]
    density = request_json["density"]
    pH = request_json["pH"]
    sulphates = request_json["sulphates"]
    alcohol = request_json["alcohol"]

    form_data = pd.read_json(
        StringIO(json.dumps(request)),
        orient="records"
        # data={
        #     "fixed acidity": fixed_acidity,
        #     "volatile acidity": volatile_acidity,
        #     "citric acid": citric_acid,
        #     "residual sugar": residual_sugar,
        #     "chlorides": chlorides,
        #     "free sulfur dioxide": free_sulfur_dioxide,
        #     "total sulfur dioxide": total_sulfur_dioxide,
        #     "density": density,
        #     "pH": pH,
        #     "sulphates": sulphates,
        #     "alcohol": alcohol,
        # }
    )

    # load the model from cloud storage

    client = storage.Client(project=PROJECT_ID)
    blobs = [
        (blob, blob.updated)
        for blob in client.list_blobs(
            "models_de2023_20204025",
        )
    ]
    latest = sorted(blobs, key=lambda tup: tup[1])[-1][0]
    latest_model = re.split("/", latest.id)[1]
    bucket = client.bucket("models_de2023_2065718")
    blob = bucket.blob(latest_model)
    with blob.open(mode="rb") as f:
        model = pickle.load(f)

    blob = bucket.blob("pca_model.pkl")
    with blob.open(mode="rb") as g:
        pca = pickle.load(g)

    blob = bucket.blob("scaler_model.pkl")
    with blob.open(mode="rb") as h:
        scaler = pickle.load(h)

    data = pd.DataFrame(
        scaler.transform(form_data),
        columns=form_data.columns,
        index=form_data.index,
    )

    X = pd.DataFrame(pca.transform(data))

    # make prediction
    # df = pd.read_json(json.dumps(request_json), orient="records")
    # print(df, file=sys.stdout)
    y_pred = model.predict(X)

    # return the response
    return jsonify({"result": str(y_pred[0])})
