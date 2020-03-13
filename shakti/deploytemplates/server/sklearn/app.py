from flask import Flask, jsonify, request
from joblib import load
from dotenv import load_dotenv

import os
import sklearn
import numpy as np
import glob

from process import preprocess, postprocess

app = Flask(__name__)
model = None


@app.before_request
def load_resources():
    '''Flask template is currently only for scikit-learn models'''
    load_dotenv()
    # in future don't make user have to write flask server themselves
    # that way don't need to use global b/c not thread-safe & using gunicorn
    global model
    if not model:
        load_model()


def load_model():
    model_type = os.getenv("MODEL_TYPE", "sklearn")
    if model_type == "sklearn":
        model_file = glob.glob(
            "*joblib")[0] if glob.glob("*joblib") else glob.glob("*pkl")[0]
        model = load(model_file)
    elif model_type == "pytorch":
        # TODO: add onnx runtime
        temp = None
    else:
        raise Exception


@app.route(os.getenv("REST_ENDPOINT", "/"))
def predict(input_data, methods=['POST']):
    transformed_input_data = preprocess(input_data)
    prediction = model.predict(transformed_input_data)
    transformed_prediction = preprocess(prediction)
    return jsonify({"prediction": transformed_prediction})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
