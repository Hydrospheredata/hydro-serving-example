import os
from flask import Flask, jsonify, request, abort
from utils import *

ADDR = "0.0.0.0"
PORT = int(os.getenv("APP_HTTP_PORT", "9090"))

MODEL_VERSION = os.getenv('MODEL_VERSION', "version")
MODEL_NAME = os.getenv('MODEL_NAME', "name")
MODEL_TYPE = os.getenv('MODEL_TYPE', "type")

app = Flask(__name__)

print("Importing TensorFlow model...")

sess, inputs, outputs = load_and_optimize("/model")


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
        feed_dict = {v.name: convert_data_to_tensor_shape(row[k], v.shape) for (k, v) in inputs.items()}

        result = sess.run(list(outputs.values()), feed_dict)

        converted_results = {k: convert_to_python(v) for k,v in zip(outputs.keys(), result)}
        merged_dict = dict(list(converted_results.items()) + list(row.items()))
        res.append(merged_dict)

    return jsonify(res)


if __name__ == '__main__':
    print("Runtime is ready to serve...")
    app.run(host=ADDR, port=PORT)
