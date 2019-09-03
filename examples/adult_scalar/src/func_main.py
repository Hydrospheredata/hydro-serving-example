import hydro_serving_grpc as hs
import numpy as np
from joblib import load

clf = load('/model/files/random-forest-adult.joblib')

features = ['age',
            'workclass',
            'education',
            'marital_status',
            'occupation',
            'relationship',
            'race',
            'sex',
            'capital_gain',
            'capital_loss',
            'hours_per_week',
            'country']


def extract_value(proto):
    return np.array(proto.int64_val, dtype='int64')[0]


def predict(**kwargs):
    extracted = np.array([extract_value(kwargs[feature]) for feature in features])
    transformed = np.dstack(extracted).reshape(1, len(features))
    predicted = clf.predict(transformed)

    response = hs.TensorProto(
        int64_val=[predicted.item()],
        dtype=hs.DT_INT64,
        tensor_shape=hs.TensorShapeProto())

    return hs.PredictResponse(outputs={"classes": response})
