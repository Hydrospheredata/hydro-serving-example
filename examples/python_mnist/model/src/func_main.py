import hydro_serving_grpc as hs
import numpy as np
import tensorflow as tf
from keras.models import load_model


def extract_value(proto):
    return np.array(proto.double_val, dtype='float64').reshape((-1, 28 * 28))


m = load_model("/model/files/model.h5", compile=False)

global graph
graph = tf.get_default_graph()


def predict(**kwargs):
    extracted = extract_value(kwargs['input'])

    with graph.as_default():
        probas = m.predict(extracted)

    classes = np.array(probas).argmax(axis=0)

    probas_proto = hs.TensorProto(
        double_val=probas.flatten().tolist(),
        dtype=hs.DT_DOUBLE,
        tensor_shape=hs.TensorShapeProto(
            dim=[hs.TensorShapeProto.Dim(size=-1), hs.TensorShapeProto.Dim(size=10)]))

    classes_proto = hs.TensorProto(
        int64_val=classes.flatten().tolist(),
        dtype=hs.DT_INT64,
        tensor_shape=hs.TensorShapeProto(
            dim=[hs.TensorShapeProto.Dim(size=-1), hs.TensorShapeProto.Dim(size=1)]))

    return hs.PredictResponse(outputs={"classes": classes_proto, "probabilities": probas_proto})