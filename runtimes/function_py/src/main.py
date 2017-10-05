import os
import urllib.request
import json
import logging
import sys
from flask import Flask, jsonify, request, abort
import importlib.util

ADDR = "0.0.0.0"
PORT = int(os.getenv("APP_HTTP_PORT", "9090"))
MODEL_NAME = os.getenv('MODEL_NAME', "pm_scikit")

FUNCTION_PATH = "/model"

sys.path.append(f"{FUNCTION_PATH}/src")

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger()
app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health():
    return "Hi"


@app.route('/<path>', methods=['POST'])
def execute(path):
    import function

    input_data = request.json
    if not input_data:
        return abort(400, "Data is empty")
    return json.dumps(function.execute(input_data, route=path))


if __name__ == '__main__':
    app.run(host=ADDR, port=PORT)
    log.info(f"Server @ {ADDR}:{PORT}")
    log.info("Function is ready to serve.")
