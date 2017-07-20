import os
import urllib.request
import json
from flask import Flask, jsonify, request, abort
from tensorflow.python.saved_model.signature_constants import DEFAULT_SERVING_SIGNATURE_DEF_KEY

from utils import *
from ml_repository import *

ADDR = os.getenv("SERVE_ADDR", "0.0.0.0")
PORT = int(os.getenv("SERVE_PORT", "9090"))

MODEL_VERSION = os.getenv('MODEL_VERSION', "version")
MODEL_NAME = os.getenv('MODEL_NAME', "name")
MODEL_TYPE = os.getenv('MODEL_TYPE', "type")

ML_REPO_ADDR = os.getenv('ML_REPO_ADDR', '0.0.0.0')
ML_REPO_PORT = os.getenv('ML_REPO_PORT', '8081')

app = Flask(__name__)
repo = MLRepository(ML_REPO_ADDR, ML_REPO_PORT)

model_cache = {}


@app.route('/health', methods=['GET'])
def health():
    return "Hi"


@app.route('/<model_name>', methods=['POST'])
def predict(model_name):
    with tf.Session() as sess:
        meta_graph = tf.saved_model.loader.load(sess, [tf.saved_model.tag_constants.SERVING], '/tmp/{0}'.format(model_name))
        signature = meta_graph.signature_def[DEFAULT_SERVING_SIGNATURE_DEF_KEY]
        inputs = list(signature.inputs._values.keys())
        outputs = list(signature.outputs._values.keys())
        input_tensors = {x: sess.graph.get_tensor_by_name(signature.inputs[x].name) for x in inputs}
        output_tensors = {x: sess.graph.get_tensor_by_name(signature.outputs[x].name) for x in outputs}

        input_raw = request.json
        input_dict = dict(zip(input_raw[0], zip(*[d.values() for d in input_raw])))
        feed_dict = {v.name: np.matrix(list(input_dict[k])) for (k, v) in input_tensors.items()}

        result = sess.run(output_tensors, feed_dict)

        converted_results = {k: v.tolist() if type(v) is np.ndarray else v for k, v in result.items()}

        merged_dict = dict(list(converted_results.items()) + list(input_dict.items()))
        res_list = [dict(zip(merged_dict, t)) for t in zip(*merged_dict.values())]

        return jsonify(res_list)


if __name__ == '__main__':
    app.run(host=ADDR, port=PORT)
