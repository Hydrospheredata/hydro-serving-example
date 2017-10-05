import os
import urllib.request
import json
from flask import Flask, jsonify, request, abort
import tensorflow as tf
import numpy as np
from tensorflow.python.saved_model.signature_constants import DEFAULT_SERVING_SIGNATURE_DEF_KEY

from utils import *

ADDR = "0.0.0.0"
PORT = int(os.getenv("APP_HTTP_PORT", "9090"))

MODEL_VERSION = os.getenv('MODEL_VERSION', "version")
MODEL_NAME = os.getenv('MODEL_NAME', "name")
MODEL_TYPE = os.getenv('MODEL_TYPE', "type")

app = Flask(__name__)

print("Loading TF model...")
sess = tf.Session()
meta_graph = tf.saved_model.loader.load(sess, [tf.saved_model.tag_constants.SERVING], '/model')
signature = meta_graph.signature_def[DEFAULT_SERVING_SIGNATURE_DEF_KEY]

inputs = list(signature.inputs.keys())
outputs = list(signature.outputs.keys())
input_tensors = {x: sess.graph.get_tensor_by_name(signature.inputs[x].name) for x in inputs}
output_tensors = {x: sess.graph.get_tensor_by_name(signature.outputs[x].name) for x in outputs}
print("Model loaded. Ready to serve.")

print("Input tensors:")
[print(x) for x in input_tensors]

print("Output tensors:")
[print(x) for x in output_tensors]


@app.route('/health', methods=['GET'])
def health():
    return "Hi"


@app.route('/<model_name>', methods=['POST'])
def predict(model_name):
    input_raw = request.json
    if not input_raw:
        return abort(400, "Data is empty")
    res = []
    for row in input_raw:
        if not set(inputs).issubset(set(row.keys())):
            print("ERROR Input columns are missing")
            return abort(400, "Input columns are missing")
        feed_dict = {v.name: convert_data_to_tensor_shape(row[k], v.shape) for (k, v) in input_tensors.items()}

        result = sess.run(output_tensors, feed_dict)

        converted_results = {k: convert_to_python(v) for k, v in result.items()}
        merged_dict = dict(list(converted_results.items()) + list(row.items()))
        res.append(merged_dict)

    return jsonify(res)


if __name__ == '__main__':
    app.run(host=ADDR, port=PORT)
