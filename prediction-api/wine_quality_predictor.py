import json
import os

import pandas as pd
from flask import jsonify
from keras.models import load_model
import logging
from io import StringIO


class WinePredictor:
    def __init__(self):
        self.model = None

    def predict_single_record(self, prediction_input):
        logging.debug(prediction_input)
        if self.model is None:
            try:
                # MODEL_REPO = /usr/src/myapp
                model_repo = os.environ['MODEL_REPO']
                #Not sure if correct, but now redirects to /usr/src/myapp/models/wine_quality_classification.ipynb
                file_path = os.path.join(model_repo, "models/wine_quality_classification.ipynb")
                self.model = load_model(file_path)
            except KeyError:
                print("MODEL_REPO is undefined")
                # When error raised, it would go to local model file, TURNED IT OFF
                #self.model = load_model('model.h5')

        # Gets input data from API call
        df = pd.read_json(StringIO(json.dumps(prediction_input)), orient='records')
        # Makes a predict call, using the model defined in the file directed above
        y_pred = self.model.predict(df)
        
        #Not sure about below, seems to determine diabeters using likelyhood
        logging.info(y_pred[0])
        
        # Makes TRUE or FALSE call
        status = (y_pred[0] > 0.5)
        logging.info(type(status[0]))
        # return the prediction outcome as a json message. 200 is HTTP status code 200, indicating successful completion
        return jsonify({'result': str(status[0])}), 200