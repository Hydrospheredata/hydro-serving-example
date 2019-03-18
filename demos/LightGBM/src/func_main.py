# coding: utf-8
# pylint: disable = invalid-name, C0111

from datetime import datetime;
import pandas as pd;
import numpy as np;
from sklearn.externals import joblib;
import json;
import hydro_serving_grpc as hs;

model = joblib.load("/model/files/forecaster.pkl");

def predict(**kwargs):

    try:

        input_data = {};

        for key, value in kwargs.items():
            input_data[key] = value.double_val;

        data_frame = pd.DataFrame.from_dict(input_data);
        prediction = model.predict(data_frame).tolist();

        prediction_tensor_shape = hs.TensorShapeProto(dim=[hs.TensorShapeProto.Dim(size=len(prediction))]);
        status_tensor_shape = hs.TensorShapeProto(dim=[hs.TensorShapeProto.Dim(size=1)]);

        status = [b"Ok"];

        return hs.PredictResponse(outputs = {"prediction": hs.TensorProto(dtype = hs.DT_DOUBLE, double_val = prediction, tensor_shape = prediction_tensor_shape), \
            "status": hs.TensorProto(dtype = hs.DT_STRING, string_val = status, tensor_shape = status_tensor_shape)});

    except Exception as exception:
        
        status = [repr(exception).encode("utf-8")]
        prediction = [0.00];
        
        tensor_shape = hs.TensorShapeProto(dim=[hs.TensorShapeProto.Dim(size=1)]);

        return hs.PredictResponse(outputs = {"prediction": hs.TensorProto(dtype = hs.DT_DOUBLE, double_val = prediction, tensor_shape = tensor_shape), \
            "status": hs.TensorProto(dtype = hs.DT_STRING, string_val = status, tensor_shape = tensor_shape)});



