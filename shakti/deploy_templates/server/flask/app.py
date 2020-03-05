import os

from flask import Flask, jsonify
from gcp_utils.googlebucket import gcs_download_file
from joblib import load

app = Flask(__name__)

model = None


@app.before_request
def load_resources():
    '''Flask template is currently only for scikit-learn models'''
    if not model:
        model = load(os.environ["MODEL_PATH"])


def transform_data(input_data):
    # no transform by default
    return input_data


@app.route('/')
def predict(input_data, methods=['POST']):
    transformed_data = transform_data(input_data)
    prediction = model.predict(transformed_data)
    return jsonify({"prediction": prediction})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
