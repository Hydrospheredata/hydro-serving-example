import os

import caffe
import numpy as np
from flask import Flask, jsonify, request, abort

ADDR = "0.0.0.0"
PORT = int(os.getenv("APP_HTTP_PORT", "9090"))

MODEL_VERSION = os.getenv('MODEL_VERSION', "version")
MODEL_NAME = os.getenv('MODEL_NAME', "name")
MODEL_TYPE = os.getenv('MODEL_TYPE', "type")

app = Flask(__name__)
print("Loading Caffe model...")
model = os.path.join('/model', 'deploy.prototxt')
weights = os.path.join('/model', 'model.caffemodel')
net = caffe.Net(model, weights, caffe.TEST)

print("Model loaded. Ready to serve.")
caffe.set_mode_cpu()

print('Input tensors:')
inputs = [(input_name, net.blobs[input_name]) for input_name in net.inputs]


@app.route('/health', methods=['GET'])
def health():
    return "Hi"


@app.route('/<model_name>', methods=['POST'])
def predict(model_name):
    input_raw = request.get_json(force=True)
    if not input_raw:
        return abort(400, "Data is empty {}".format(input_raw))
    if set(input_raw.keys()) != set(net.inputs):
        return abort(400, "Data has incorrect inputs expected {} but got {}".format(net.inputs, input_raw.keys()))
    data = dict([(k, np.array(v)) for k, v in input_raw.items()])
    res = net.forward_all(**data)
    return jsonify(dict([(k, v.tolist()) for k, v in res.items()]))


if __name__ == '__main__':
    app.run(host=ADDR, port=PORT)
