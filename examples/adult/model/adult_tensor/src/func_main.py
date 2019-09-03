import hydro_serving_grpc as hs
import numpy as np
from joblib import load

clf = load('/model/files/random-forest-adult.joblib')


def extract_value(proto):
    return np.array(proto.int64_val, dtype='int64').reshape([dim.size for dim in proto.tensor_shape.dim])


def predict(**kwargs):
    x = extract_value(kwargs['input'])
    predicted = clf.predict(x)

    response = hs.TensorProto(
        int64_val=predicted.flatten().tolist(),
        dtype=hs.DT_INT64,
        tensor_shape=hs.TensorShapeProto(
            dim=[hs.TensorShapeProto.Dim(size=-1), hs.TensorShapeProto.Dim(size=1)]))

    return hs.PredictResponse(outputs={"classes": response})
