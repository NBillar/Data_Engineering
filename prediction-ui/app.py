# importing Flask and other modules
import json
import os
import logging
import requests
from flask import Flask, request, render_template, jsonify

# Flask constructor
app = Flask(__name__)


# A decorator used to tell the application
# which URL is associated function
@app.route("/checkwinequality", methods=["GET", "POST"])
def check_wine_quality():
    if request.method == "GET":
        return render_template("input_form_page.html")

    elif request.method == "POST":
        prediction_input = {
            "fixed acidity": float(request.form.get("fixed-acidity")),
            "volatile acidity": float(request.form.get("volatile-acidity")),
            "citric acid": float(request.form.get("citric-acid")),
            "residual sugar": float(request.form.get("residual-sugar")),
            "chlorides": float(request.form.get("chlorides")),
            "free sulfur dioxide": int(request.form.get("free-sulfur-dioxide")),
            "total sulfur dioxide": int(request.form.get("total-sulfur-dioxide")),
            "density": float(request.form.get("density")),
            "pH": float(request.form.get("pH")),
            "sulphates": float(request.form.get("sulphates")),
            "alcohol": float(request.form.get("alcohol")),
        }

        logging.debug("Prediction input : %s", prediction_input)

        # use requests library to execute the prediction service API by sending an HTTP POST request
        # use an environment variable to find the value of the diabetes prediction API
        # json.dumps() function will convert a subset of Python objects into a json string.
        # json.loads() method can be used to parse a valid JSON string and convert it into a Python Dictionary.

        predictor_api_url = os.environ["PREDICTOR_API"]
        res = requests.post(predictor_api_url, json=prediction_input)

        prediction_value = res.json()["result"]
        logging.info("Prediction Output : %s", prediction_value)
        return render_template(
            "response_page.html", prediction_variable=prediction_value
        )

    else:
        return jsonify(message="Method Not Allowed"), 405

    # that our app that does not allow the users to perform any other HTTP method (e.g., PUT and  DELETE) for
    # '/checkdiabetes' path


# prediction-ui-3f56v4iscq-uc.a.run.app/checkdiabetes

# The code within this conditional block will only run the python file is executed as a
# script. See https://realpython.com/if-name-main-python/
if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 5000)), host="0.0.0.0", debug=True)
