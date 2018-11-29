import numpy as np
import hydro_serving_grpc as hs
from sklearn.externals import joblib

clf = joblib.load('/model/files/rf.joblib.pkl')


def infer(features):
    data = np.array(features.double_val) \
        .reshape([dim.size for dim in features.tensor_shape.dim])
    prediction = clf.predict(data)

    guess_shape = hs.TensorShapeProto(
        dim=[hs.TensorShapeProto.Dim(size=item) for item in prediction.shape])
    guess = hs.TensorProto(
        dtype=hs.DT_BOOL,
        bool_val=prediction,
        tensor_shape=guess_shape)
    return hs.PredictResponse(outputs={'is_fraud': guess})