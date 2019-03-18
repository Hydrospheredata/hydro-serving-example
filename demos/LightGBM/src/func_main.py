# coding: utf-8
# pylint: disable = invalid-name, C0111

from datetime import datetime;
import pandas as pd;
import numpy as np;
from sklearn.externals import joblib;
import json;
import hydro_serving_grpc as hs;

model = joblib.load("/model/files/forecaster.pkl");

def predict(input_data):

    try:
        samples_list = [];

        for sample_json in input_data.string_val:
            sample_dict = json.loads(sample_json);
            samples_list.append(sample_dict);

        data_frame = pd.DataFrame.from_dict(samples_list);

        prediction = model.predict(data_frame).tolist();
        tensor_shape = hs.TensorShapeProto(dim=[hs.TensorShapeProto.Dim(size=len(samples_list))]);

    except Exception as exception:
        print(exception);
        prediction = [0.00];
        tensor_shape = hs.TensorShapeProto(dim=[hs.TensorShapeProto.Dim(size=1)]);

    

    return hs.PredictResponse(outputs = {"prediction": hs.TensorProto(dtype = hs.DT_FLOAT, float_val = prediction, tensor_shape = tensor_shape)});



