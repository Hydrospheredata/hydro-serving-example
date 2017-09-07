import os
import urllib.request
import json
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request, abort
from sklearn.externals import joblib

import logging
import sys
from scikit_metadata import *
from utils import *

ADDR = "0.0.0.0"
PORT = int(os.getenv("APP_HTTP_PORT", "9090"))
MODEL_NAME = os.getenv('MODEL_NAME', "pm_scikit")

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger()
app = Flask(__name__)
log.info("Server @ {0}:{1}".format(ADDR, PORT))
log.info("Model is loaded and ready to serve.")

with open("/model/metadata.json") as file:
    metadata = json.load(file)
pipeline = joblib.load("/model/model.pkl")
input_columns = metadata['inputs']
output_columns = metadata['outputs']

@app.route('/health', methods=['GET'])
def health():
    return "Hi"


@app.route('/<model_name>', methods=['POST'])
def predict(model_name):
    input_data = request.json
    if not input_data:
        return abort(400, "Data is empty")
    input_data_keys = list(input_data[0].keys())
    if not set(input_columns).issubset(set(input_data_keys)):
        log.info("ERROR Input columns are missing")
        abort(400, "Input columns are missing")
    df = dict_to_df(input_data, input_columns)
    log.info(df)
    prediction = pipeline.predict(df[input_columns])
    res_df = pd.DataFrame(data=prediction, columns=output_columns)
    log.info(str(df) + '\nPrediction:\n' + str(res_df))
    return jsonify(df_to_json(df.join(res_df)))


if __name__ == '__main__':
    app.run(host=ADDR, port=PORT)
