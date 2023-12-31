import os

from flask import Flask, request

from winequality_predictor import predict_wine_quality  # [IMPORTS MODEL FUNCTION]

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route(
    "/wine_quality_predictor/", methods=["POST"]
)  # path of the endpoint. Except only HTTP POST request
def predict_str():
    # the prediction input data in the message body as a JSON payload
    prediction_inout = request.get_json()
    return predict_wine_quality(
        request=prediction_inout, PROJECT_ID=os.environ["PROJECT_ID"]
    )


# The code within this conditional block will only run the python file is executed as a
# script. See https://realpython.com/if-name-main-python/
if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 5000)), host="0.0.0.0", debug=True)
